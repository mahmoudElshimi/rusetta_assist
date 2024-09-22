from datetime import timedelta

from odoo import api, fields, models

from odoo.exceptions import ValidationError


class Attendance(models.Model):
    _name = "rusetta.attendance"
    _description = "Attendance Record"
    _sql_constraints = [
        (
            "unique_attenance",
            "unique(date, grade, place_id, teacher_id)",
            "يوجد بالفعل سجل حضور بهذه البيانات.",
        )
    ]
    date = fields.Date("التاريح", default=fields.Date.today)
    teacher_id = fields.Many2one("rusetta.teacher", string="المدرس", required=True)
    student_ids = fields.Many2many("rusetta.student", string="الطلاب")
    place_id = fields.Many2one("rusetta.place", string="المكان", required=True)
    name = fields.Char(compute="_compute_name", store=True, string="العنوان")
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

    @api.depends("place_id.name", "date", "grade")
    def _compute_name(self):
        for record in self:
            grade_display = dict(self._fields["grade"].selection).get(record.grade)
            record.name = f"{record.place_id.name} ({grade_display}) - {record.date}"

    @api.constrains("date")
    def _check_date_end(self):
        for record in self:
            if record.date > fields.Date.today():
                raise ValidationError(
                    f"لقد ادخلت تاريخ {record.date} ما بك لا يمكن عمل  سجل مستقبلي!"
                )

    @api.model
    def create(self, vals):
        record = super(Attendance, self).create(vals)
        # After creating the attendance, update the last_seen field for students
        if record.student_ids:
            record.student_ids.write({"last_seen": record.date})
        return record

    def write(self, vals):
        res = super(Attendance, self).write(vals)
        # After updating the attendance, update the last_seen field for students
        if "student_ids" in vals or "date" in vals:
            for record in self:
                if record.student_ids:
                    record.student_ids.write({"last_seen": record.date})
        return res
