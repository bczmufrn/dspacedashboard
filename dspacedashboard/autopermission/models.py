from django.db import models

from dspacedashboard.core.models import BaseModel
from dspacedashboard.autopermission import ufrn, dspace

class AutoPermissionUserManager(models.Manager):
	def search(self, query):
		return self.filter(
            netid__icontains=query
        )

class AutoPermissionUser(BaseModel):
    netid = models.CharField('Login LDAP', max_length=255)
    created = models.BooleanField('Usuário criado no DSpace', default=False)
    api_response = models.JSONField('Retorno da API', null=True, blank=True)

    objects = AutoPermissionUserManager()

    class Meta:
        verbose_name = 'Registro de permissionamento'
        verbose_name_plural = 'Registros de permissionamento'
        ordering = ('-created_at', )

    def __str__(self):
        return self.netid
    
    def update_dspace_user(self):
        courses = ufrn.load_courses()
        student_details = ufrn.get_user_details(self.netid)

        if not student_details.get('course_id', None):
            self.api_response = {'error': 'Nenhum curso retornado para o usuário'}
            self.save()
            return
        
        self.api_response = student_details
        
        dspace_course = list(filter(lambda course: int(course['id_curso']) == int(student_details['course_id']), courses))
        if not dspace_course:
            self.api_response = {
                'error': f"SIGAA course {student_details['course_name']} ({student_details['course_id']}) not found"
            }
            self.save()
            return
        
        if not dspace_course[0]['grupo_dspace']:
            self.api_response = {'error': f"SIGAA course {dspace_course[0]['nome']} has no dspace_group"}
            return
        
        dspace_courses = dspace_course[0]['grupo_dspace'].split(',')

        try:
            for _dspace_course in dspace_courses:
                dspace.update_dspace_user(self.netid, ["-G", _dspace_course.strip()])
            self.created = True
        except Exception as e:
            self.created = False

        self.save()