
import { useState } from "react";
import "./App.css";

function App() {
  const [candidateName, setCandidateName] = useState("");
  const [result, setResult] = useState(null);
  function downloadResults() {
  if (!result) {
    alert("Please evaluate a candidate first.");
    return;
  }

  const fileContent = JSON.stringify(
    {
      candidate_name: candidateName,
      ...result,
    },
    null,
    2
  );

  const blob = new Blob([fileContent], {
    type: "application/json",
  });

  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");

  link.href = url;
  link.download = "radix-talent-results.json";
  link.click();

  URL.revokeObjectURL(url);
}
  function resetForm() {
  setCandidateName("");
  setResult(null);
  document.getElementById("profileFile").value = "";
  document.getElementById("companyFile").value = "";
}
  
async function evaluateTalent() {
  const profileFile = document.getElementById("profileFile").files[0];
  const companyFile = document.getElementById("companyFile").files[0];
  if (!candidateName.trim()) {
  alert("Please enter the candidate's name.");
  return;
}

 if (!profileFile && !companyFile) {
  alert("Please upload both the candidate profile and company requirements JSON files.");
  return;
}

if (!profileFile) {
  alert("Please upload the candidate profile JSON file.");
  return;
}

if (!companyFile) {
  alert("Please upload the company requirements JSON file.");
  return;
}

  const formData = new FormData();
  formData.append("profile_file", profileFile);
  formData.append("company_file", companyFile);
  formData.append("benchmark_mode", "synthetic");

  try {
    const response = await fetch(
      "http://127.0.0.1:8000/api/team/v1/talent-check/evaluate",
      {
        method: "POST",
        body: formData,
      }
    );

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "Evaluation failed.");
    }

    setResult(data);
  } catch (error) {
    alert(
  error.message ||
    "Unable to evaluate talent. Please check that the backend server is running and try again."
);
  }
}


  return (
    <div className="app">
      <header className="header">
        <h1>RADIX</h1>
        <span>Talent Check</span>
      </header>

      <main className="main">
        <p className="eyebrow">MODULE 4</p>
        <h2>Talent Readiness Assessment</h2>
        <p className="description">
          Evaluate candidate skills against company requirements.
        </p>

        <section className="card">
          <h3>Candidate Details</h3>
          <label htmlFor="candidateName">Candidate Name</label>
          <input
            id="candidateName"
            type="text"
            placeholder="Enter candidate name"
            value={candidateName}
            onChange={(event) => setCandidateName(event.target.value)}
          />
          <label htmlFor="profileFile">Candidate Profile (JSON)</label>
<input
  id="profileFile"
  type="file"
  accept=".json"
/>

<label htmlFor="companyFile">Company Requirements (JSON)</label>
<input
  id="companyFile"
  type="file"
  accept=".json"
/>
          <button onClick={evaluateTalent}>
          Get Started
          </button>
          <button type="button" onClick={resetForm}>
  Reset
</button>
        </section>
        

{result && (
  <section className="card">
    <h3>Talent Readiness Result</h3>
   
    <p>
  <strong>Candidate Name:</strong> {candidateName || "Not provided"}
</p>

    <p>Overall Readiness</p>
    <h2>{result.readiness_score ?? 0}%</h2>

    <div className="progress-track">
      <div
        className="progress-fill"
        style={{ width: `${result.readiness_score ?? 0}%` }}
      />
    </div>

    <p>
      Skills evaluated: {result.rating_completeness ?? 0}
    </p>

    <h3>Skill Gap Analysis</h3>

    <div className="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Skill</th>
            <th>Candidate</th>
            <th>Required</th>
            <th>Shortfall</th>
          </tr>
        </thead>
        <tbody>
          {(result.skillset_gap ?? []).map((skill) => (
            <tr key={skill.category_code}>
              <td>{skill.skill_name}</td>
              <td>{skill.candidate_level}</td>
              <td>{skill.required_level}</td>
              <td>
  <span
    className={
      skill.shortfall === 0
        ? "gap-low"
        : skill.shortfall <= 2
        ? "gap-medium"
        : "gap-high"
    }
  >
    {skill.shortfall}
  </span>
</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
           <button onClick={downloadResults}>
  Download Results
</button>
    <p className="notice">
      {result.notice}
    </p>
  </section>
)}


        <p className="notice">
          Practice interface — synthetic company benchmarks are fictional.
        </p>
      </main>
    </div>
  );
}

export default App;
