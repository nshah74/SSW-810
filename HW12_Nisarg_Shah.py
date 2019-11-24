from flask import Flask, render_template

app = Flask(__name__)

@app.route('/students')

def student_courses():
    import sqlite3
    dbpath = "C:/810/Stevens/810_startup.db"
    try:
        db = sqlite3.connect(dbpath)
    except sqlite3.OperationalError:
        return f"Error: Unable to open database at {dbpath}"
    else:
        query = """select Ins.CWID, Ins.Name , Ins.Dept, Gra.Course, count(*) as Students from instructors Ins join grades Gra  on Ins.CWID = Gra.InstructorCWID
                GROUP BY Gra.InstructorCWID,Gra.Course;"""
        data = [{"CWID":CWID, "Name":Name, "Dept":Dept, "Course":Course, "Student":Student} 
        for CWID, Name, Dept, Course, Student in db.execute(query)]
        db.close()
        
        return render_template('student_courses.html', 
        title="Stevens Data Repository", 
        table_title="Students Course Completion", data=data)


app.run(debug=True)