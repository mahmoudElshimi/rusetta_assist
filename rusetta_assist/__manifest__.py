{
    "name": "Rusetta Assist",
    "summary": "Educational Platform",
    "depends": ["base"],
    "author": "Mahmoud ElShimi",
    "website": "mailto:mahmoudelshimi@protonmail.ch",
    "category": "Education",
    "version": "1.0",
    "license": "Other proprietary",  # See LICENSE(MIT/X) File in the same dir.
    "images": [
            "images/student.png"
            "images/attendance.png"
            "images/exam.png"
            "static/description/banner.png",
            "images/banner.png",
    ],

    "data": [
        "security/ir.model.access.csv",
        "views/rusetta_actions.xml",
        "views/rusetta_menus.xml",
        "views/rusetta_student_views.xml",
        "views/rusetta_teacher_views.xml",
        "views/rusetta_attendance_views.xml",
        "views/rusetta_place_views.xml",
        "views/rusetta_exam_views.xml",
        "views/rusetta_exam_mark_views.xml",
    ],
    "installable": True,
    "application": True,
}
