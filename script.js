async function predictSalary() {
    const Age = parseInt(document.getElementById("Age").value);
    const Gender = document.getElementById("Gender").value;
    const EducationLevel = document.getElementById("Education Level").value;  
    const JobTitle = document.getElementById("Job Title").value;
    const Experience = parseFloat(document.getElementById("Experience").value);

    if (isNaN(Age) || isNaN(Experience) || !Gender || !EducationLevel || !JobTitle) {
        document.getElementById("predictionSalary").textContent = "Please enter valid inputs to get the salary prediction.";
        return;
    }

    const inputData = {
        "Age": Age,
        "Gender": Gender,
        "Education Level": EducationLevel, 
        "Job Title": JobTitle,
        "Years of Experience": Experience
    };

    try {
        const response = await fetch('http://127.0.0.1:5000/predict', {  
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ input: inputData })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();

        if (data.error) {
            document.getElementById("predictionSalary").textContent = "Error: " + data.error;
        } else {
            document.getElementById("predictionSalary").textContent = `Predicted Salary: ${data.Salary}`;
        }

    } catch (error) {
        console.error("Error predicting salary:", error);
        document.getElementById("predictionSalary").textContent = "Error predicting salary. Check console.";
    }
}
