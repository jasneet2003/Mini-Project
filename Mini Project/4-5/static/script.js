document.addEventListener("DOMContentLoaded", function() {
    const studentRows = document.querySelectorAll(".student-row");
    let currentIndex = 0;

    // Hide all student rows except the first one
    studentRows.forEach((row, index) => {
        if (index !== currentIndex) {
            row.style.display = "none";
        }
    });

    // Handle keydown event
    document.addEventListener("keydown", function(event) {
        if (event.keyCode === 32) { // Space key
            markAttendance("present");
        } else if (event.keyCode === 8) { // Backspace key
            markAttendance("absent");
        }
    });

    function markAttendance(status) {
        // Get the radio button element for the current student
        const radioButtons = studentRows[currentIndex].querySelectorAll("input[type='radio']");
        const radioButton = status === "present" ? radioButtons[0] : radioButtons[1];

        // Mark the attendance
        radioButton.checked = true;

        // Hide current row
        studentRows[currentIndex].style.display = "none";

        // Move to the next row
        currentIndex++;

        if (currentIndex < studentRows.length) {
            // Show the next row
            studentRows[currentIndex].style.display = "table-row";
        } else {
            // If all rows are processed, submit the form
            document.getElementById("attendanceForm").submit();
        }
    }
});
