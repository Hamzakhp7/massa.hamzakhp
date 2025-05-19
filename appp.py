from flask import Flask, render_template, request

app = Flask(name)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    math_result = None
    final_avg = None

    # معالجة المراقبة المستمرة للمواد
    if "submit_main" in request.form:
        try:
            grades = []
            for i in range(1, 5):
                val = request.form.get(f"grade{i}")
                if val.strip() != "":
                    grades.append(float(val))
            activities = float(request.form.get("activities"))
            if grades:
                average = sum(grades) / len(grades)
                result = round((average * 0.75) + (activities * 0.25), 2)
        except:
            result = "خطأ في الإدخال"

        try:
            math_grades = []
            for i in range(1, 4):
                val = request.form.get(f"math{i}")
                if val.strip() != "":
                    math_grades.append(float(val))
            if math_grades:
                math_result = round(sum(math_grades) / len(math_grades), 2)
        except:
            math_result = "خطأ في الإدخال"

    # معالجة المعدل النهائي
    final_subjects_data = [
        {"name": "المواضبة و السلوك", "coeff": 1},
        {"name": "التربية الإسلامية", "coeff": 2},
        {"name": "التربية البدنية", "coeff": 4},
        {"name": "الرياضيات", "coeff": 7},
        {"name": "الفلسفة", "coeff": 2},
        {"name": "الفيزياء والكيمياء", "coeff": 7},
        {"name": "اللغة الانجليزية", "coeff": 2},
        {"name": "اللغة العربية", "coeff": 2},
        {"name": "اللغة الفرنسية", "coeff": 4},
        {"name": "علوم الحياة و الأرض", "coeff": 5},
    ]
    final_subjects = []

    if "submit_final" in request.form:
        total_score = 0
        total_coeff = 0
        for idx, item in enumerate(final_subjects_data):
            grade_str = request.form.get(f"final_{idx}", "").strip()
            grade = float(grade_str) if grade_str else None
            total = round(grade * item["coeff"], 2) if grade is not None else None
            final_subjects.append({
                "name": item["name"],
                "coeff": item["coeff"],
                "grade": grade_str,
                "total": total
            })
            if grade is not None:
                total_score += total
                total_coeff += item["coeff"]

        final_avg = round(total_score / total_coeff, 2) if total_coeff else None
    else:
        final_subjects = [{"name": item["name"], "coeff": item["coeff"], "grade": "", "total": None} for item in final_subjects_data]

    return render_template("index.html", result=result, math_result=math_result,
                           final_subjects=final_subjects, final_avg=final_avg)

if name == "main":
    app.run(debug=True)