from odoo import fields, models


class Place(models.Model):
    _name = "rusetta.place"
    _description = "المكان"
    name = fields.Char("الأماكن", required=True)
    type_ = fields.Selection(
        string="النوع",
        selection=[
            ("center", "سنتر"),
            ("school", "مدرسة"),
            ("private", "خاص"),
            ("online", "أونلاين"),
        ],
        required=True,
        default="center",
    )
    student_ids = fields.Many2many("rusetta.student", string="الطلاب")
    teacher_ids = fields.Many2many("rusetta.teacher", string="المدرسون")
    attendance_ids = fields.One2many(
        "rusetta.attendance", "place_id", string="سجلات الحضور"
    )
    _sql_constraints = [
        (
            "unique_name",
            "unique(name)",
            "يوجد بالفعل مكان بهئا الاسم",
        )
    ]
