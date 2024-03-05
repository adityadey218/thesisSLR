from django.db import models
from ..models.literatureCl import LiteratureCl
from ..models.recommendetLit import RecommendetLit


class Mendeley(models.Model):
    Literature_id = models.ForeignKey(LiteratureCl, on_delete=models.CASCADE)
    #recLiterature_id = models.ForeignKey(RecommendetLit, on_delete=models.CASCADE)
    reader_count = models.IntegerField(blank=True, null=True)
    reader_count_by_academic_status = models.CharField(max_length=5000, blank=True, null=True)

    StdPostgraduate_count = models.IntegerField(blank=True, null=True)
    ProfessorAssociatProf_count = models.IntegerField(blank=True, null=True)
    Researcher_count = models.IntegerField(blank=True, null=True)
    StdMaster_count = models.IntegerField(blank=True, null=True)
    StdPhd_count = models.IntegerField(blank=True, null=True)
    Professor_count = models.IntegerField(blank=True, null=True)
    StdBachelor_count = models.IntegerField(blank=True, null=True)
    StdDoctoralstd_count = models.IntegerField(blank=True, null=True)
    Lecturer_count = models.IntegerField(blank=True, null=True)
    Other_count = models.IntegerField(blank=True, null=True)
    Librarian_count = models.IntegerField(blank=True, null=True)
    LecturerSeniorLec_count = models.IntegerField(blank=True, null=True)
    Unspecified_count = models.IntegerField(blank=True, null=True)
    reader_count_by_subject_area = models.CharField(max_length=5000, blank=True, null=True)
    reader_count_by_subdiscipline = models.CharField(max_length=5000, blank=True, null=True)
    reader_count_by_country = models.CharField(max_length=5000, blank=True, null=True)
    group_count = models.IntegerField(blank=True, null=True)
    has_pdf = models.CharField(max_length=500, null=True)

