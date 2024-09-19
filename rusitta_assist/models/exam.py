from odoo import api, fields, models
from odoo.exceptions import ValidationError


class Exam(models.Model):
    _name = "rusetta.exam"
    _description = "Exam Record"
    date = fields.Date("التاريخ", default=fields.Date.today)
    teacher_id = fields.Many2one("rusetta.teacher", string="المدرس", required=True)
    name = fields.Char(compute="_compute_name", store=True, string="العنوان")
    number = fields.Integer("رقم الامتحان", required=True, default=0)
    student_ids = fields.One2many("rusetta.student", "exam_id", string="الطلاب")

    # Course and grade
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

    course = fields.Selection(
        selection=[
            ("نحو", "نحو"),
            ("بلاغة", "بلاغة"),
            ("أدب", "أدب"),
            ("نصوص متحررة", "نصوص متحررة"),
            ("قراءة متحررة", "قراءة متحررة"),
            ("تعبير", "تعبير"),
            ("قصة", "قصة"),
        ],
        string="المادة",
        required=True,
        default="نحو",
    )

    # Semester and marks
    semester = fields.Selection(
        selection=[
            ("1", "الفصل الدراسي الأول"),
            ("2", "الفصل الدراسي الثاني"),
        ],
        string="الفصل الدراسي",
        required=True,
        default="1",
    )

    full_mark = fields.Integer("الدرجة الكاملة", required=True, default=100)
    exam_mark_ids = fields.One2many(
        "rusetta.exam.mark", "exam_id", string="علامات الطلاب"
    )
    student_mark_ids = fields.One2many(
        "rusetta.exam.mark", "student_id", string="درجات الطلاب"
    )

    # Compute the exam name for easy display
    @api.depends("date", "grade", "course")
    def _compute_name(self):
        for record in self:
            grade_display = dict(self._fields["grade"].selection).get(record.grade)
            record.name = f"{grade_display}: {record.course} - {record.number}"

    # Ensure exam number is unique for the same course, grade, and semester
    _sql_constraints = [
        (
            "unique_exam_number",
            "unique(teacher_id,number, course, grade, semester)",
            "يوجد بالفعل امتحان بنفس الرقم للمادة والصف والفصل الدراسي.",
        )
    ]


"""
    @api.constrains("number")
    def _check_exam_number(self):
        for record in self:
            # Ensure the exam number doesn't conflict with another exam in the same course, grade, and semester
            existing_exam = self.search([
                ('number', '=', record.number),
                ('course', '=', record.course),
                ('grade', '=', record.grade),
                ('semester', '=', record.semester),
                ('id', '!=', record.id),
            ])
            if existing_exam:
                raise ValidationError(f"يوجد بالفعل امتحان بنفس الرقم للمادة '{record.course}', الصف '{record.grade}', والفصل الدراسي '{record.semester}'.")

"""
