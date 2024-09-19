from odoo import fields, models


class Teacher(models.Model):
    _name = "rusetta.teacher"
    _description = "Teacher"
    name = fields.Char("المدرس", required=True)
    image = fields.Image(string="Image")  # Add this line to include an image field
    attendance_ids = fields.One2many(
        "rusetta.attendance", "teacher_id", string="سجلات الحضور"
    )
    exam_ids = fields.One2many("rusetta.exam", "teacher_id", string="الامتحانات")
    student_ids = fields.Many2many("rusetta.student", string="الطلاب")
    place_ids = fields.Many2many("rusetta.place", string="اﻷماكن")
    exam_mark_ids = fields.One2many(
        "rusetta.exam.mark", "exam_teacher_id", string="علامات الطلاب"
    )
    _sql_constraints = [
        (
            "unique_name",
            "unique(name)",
            "يوجد بالفعل مدرس بهذا الاسم",
        )
    ]
