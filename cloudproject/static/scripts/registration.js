document.addEventListener("DOMContentLoaded", () => {
    const courses = JSON.parse(document.getElementById("courses-data").textContent);
    sortCourses("dragarea");
    resetSchedule()

    function resetSchedule() {
        const days = ["อาทิตย์", "จันทร์", "อังคาร", "พุธ", "พฤหัสบดี", "ศุกย์", "เสาร์"];
        const tbody = document.getElementById("schedule");
        tbody.innerHTML = "";
        days.forEach(day => {
            const tr = document.createElement("tr");
            tr.id = day;
            const th = document.createElement("th");
            th.textContent = day;
            tr.appendChild(th);
            for (i=0; i<12; i++) {
                const td = document.createElement("td");
                tr.appendChild(td);
            }
            tbody.appendChild(tr);
        })
    }
    
    function createCell(text = "") {
        const td = document.createElement("td");
        td.textContent = text;
        return td;
    }

    function createCourseRow(course) {
        const tr = document.createElement("tr");
        tr.id = course.code;
        tr.className = "hover:bg-gray-200";

        tr.appendChild(createCell(course.code));
        tr.appendChild(createCell(course.name));
        tr.appendChild(createCell(course.credits));

        const tdSection = document.createElement("td");
        const select = document.createElement("select");
        select.dataset.courseCode = course.code;

        const defaultOpt = new Option("เลือก", "no", true, true);
        select.add(defaultOpt);

        course.sections.forEach(sec => {
            select.add(new Option(sec.section_number, sec.section_number));
        });

        select.addEventListener("change", secChange);
        tdSection.appendChild(select);
        tr.appendChild(tdSection);

        let teachertext = "";
        course.teachers.forEach(teacher => {
            teachertext += teacher.title + " " + teacher.first_name + " " + teacher.last_name + "\n"
        })
        tr.appendChild(createCell(teachertext));


        tr.appendChild(createCell()); // time
        tr.appendChild(createCell()); // location
        tr.appendChild(createCell()); // capacity
        tr.appendChild(createCell()); // enrolled

        const tdRemove = createCell();
        const btn = document.createElement("button");
        btn.type = "button";
        btn.textContent = "remove";
        btn.className = "bg-red-500 hover:bg-red-700 text-white";
        btn.addEventListener("click", removeCorse);
        tdRemove.appendChild(btn);
        tr.appendChild(tdRemove);

        return tr;
    }

    function dropHandler(event) {
        event.preventDefault();
        const id = event.dataTransfer.getData("id");
        const course = courses.find(c => c.code === id);
        if (!course) return;

        document.getElementById(id).remove();
        document.getElementById("droparea").appendChild(createCourseRow(course));
        sortCourses("droparea");
    }

    function removeCorse(event) {
        const tr = event.target.closest("tr");
        const course = courses.find(c => c.code === tr.id);
        if (!course) return;

        const dragRow = document.createElement("tr");
        dragRow.id = course.code;
        dragRow.className = "hover:bg-gray-200 cursor-pointer";
        dragRow.draggable = true;
        dragRow.addEventListener("dragstart", e => e.dataTransfer.setData("id", course.code));

        dragRow.appendChild(createCell(course.code));
        dragRow.appendChild(createCell(course.name));
        dragRow.appendChild(createCell(course.credits));

        document.getElementById("dragarea").appendChild(dragRow);
        tr.remove();
        sortCourses("dragarea");
        resetSchedule();
        updateSchedule();
    }

    function secChange(event) {
        const code = event.target.dataset.courseCode;
        const sectionNum = event.target.value;
        if (sectionNum === "no") return;

        const course = courses.find(c => c.code === code);
        const section = course.sections.find(s => Number(s.section_number).toString() === sectionNum);
        if (!section) return;

        const tr = event.target.closest("tr");

        let timetext = "";
        let locationtext = "";
        section.section_class.forEach(section_class => {
            timetext += section_class.day + ": " + section_class.start_time + "-" + section_class.end_time + ", ";
            locationtext += section_class.location + "\n";
        })
        tr.children[5].textContent = timetext;
        tr.children[6].textContent = locationtext;
        tr.children[7].textContent = section.capacity;
        tr.children[8].textContent = section.enrolled_count;
        if (event.target.children[0].value === "no") event.target.children[0].remove();
        resetSchedule();
        updateSchedule();
    }

    function sortCourses(id) {
        const area = document.getElementById(id);
        [...area.children]
            .sort((a, b) => a.id.localeCompare(b.id))
            .forEach(el => area.appendChild(el));
    }

    function updateSchedule() {
        const droparea = document.getElementById("droparea");
        const schedule = document.getElementById("schedule");
        for (i=0; i<droparea.children.length; i++) {
            const tr = droparea.children[i];
            if (tr.children[3].children[0].value === "no") continue;
            const course = courses.find(c => c.code === tr.id);
            const section = course.sections.find(s => String(s.section_number) === tr.children[3].children[0].value);
            section.section_class.forEach(sc => {
                const tr = document.getElementById(sc.day);
                const start_num = Number(String(sc.start_time).slice(0, 2))
                tr.children[start_num-7].textContent = course.name;
            })
        }
    }

    document.getElementById("dragarea").addEventListener("dragstart", (e) => {
        if (e.target.tagName === "TR") {
            e.dataTransfer.setData("id", e.target.id);
        }
    });
    document.querySelector("table[ondrop]").addEventListener("drop", dropHandler);
    document.querySelector("table[ondragover]").addEventListener("dragover", e => e.preventDefault());
});
