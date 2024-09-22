from odoo import api, fields, models

from odoo.exceptions import ValidationError


class ExamMarks(models.Model):
    _name = "rusetta.exam.mark"
    _description = "Exam Marks"
    _sql_constraints = [
        (
            "unique_student_exam",
            "unique(student_id, exam_id)",
            "لا يمكن للطالب أن يأخذ نفس الامتحان أكثر من مرة.",
        ),
    ]
    mark = fields.Integer("الدرجة", required=True)
    student_id = fields.Many2one("rusetta.student", string="الطالب", required=True)
    exam_id = fields.Many2one("rusetta.exam", string="الامتحان", required=True)
    exam_name = fields.Char(
        string="اسم الامتحان", store=True, related="exam_id.name", readonly=True
    )

    exam_teacher_id = fields.Many2one(
        related="exam_id.teacher_id", store=True, readonly=True, string="المدرس"
    )
    exam_full_mark = fields.Integer(
        "الدرجة الكاملة",
        related="exam_id.full_mark",
        readonly=True,
        store=True,
    )

    exam_date = fields.Date(
        string="تاريخ الامتحان",
        related="exam_id.date",
        readonly=True,
        store=True,
    )

    @api.constrains("mark", "exam_full_mark")
    def _check_mark(self):
        for record in self:
            if record.mark < 0 or record.mark > record.exam_full_mark:
                raise ValidationError(
                    "لا يمكن أن تكون الدرجة أقل من الصفر أو أكبر من الدرجة النهائية"
                )
