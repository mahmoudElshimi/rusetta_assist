from odoo import api, fields, models
from odoo.exceptions import ValidationError


class Student(models.Model):
    _name = "rusetta.student"
    _description = "Student"
    name = fields.Char("الطالب", required=True)
    comment = fields.Char("ملاحظات", required=False)
    last_seen = fields.Date("آخر حضور", default=fields.Date.today)
    number = fields.Char("رقم الطالب", required=True, default=None)
    number_parent = fields.Char("رقم ولي الأمر", required=False, default=None)
    is_still = fields.Boolean(
        "أما زال؟", default=True, required=True, help="هل الطالب ما زال يحضر أم لا؟"
    )
    teacher_ids = fields.Many2many("rusetta.teacher", string="المدرسون")
    attendance_ids = fields.Many2many("rusetta.attendance", string="سجلات الحضور")
    exam_id = fields.Many2one("rusetta.exam", string="الامتحانات")
    place_ids = fields.Many2many("rusetta.place", string="اﻷماكن")
    grade = fields.Selection(
        selection=[
            ("12", "3ث"),
            ("11", "2ث"),
            ("10", "1ث"),
            ("9", "3ع"),
            ("8", "2ع"),
            ("7", "1ع"),
            ("6", "6ب"),
            ("5", "5ب"),
            ("4", "4ب"),
            ("3", "3ب"),
            ("2", "2ب"),
            ("1", "1ب"),
        ],
        string="الصف",
        required=True,
        default="12",
    )
    exam_mark_ids = fields.One2many(
        "rusetta.exam.mark", "student_id", string="علامات الطلاب"
    )
    _sql_constraints = [
        (
            "unique_name",
            "unique(number)",
            "يوجد بالفعل طالب بهذا الرقم",
        )
    ]

    @api.constrains("mobile_number")
    def _check_mobile_number(self):
        for record in self:
            # Regular expression for exactly 10 digits
            if record.mobile_number and not re.match(r"^\d{11}$", record.mobile_number):
                raise ValidationError("رقم الجوال غير صحيح. يجب أن يتكون من 11 أرقام.")
