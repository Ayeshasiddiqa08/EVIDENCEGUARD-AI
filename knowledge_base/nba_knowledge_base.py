"""
EvidenceGuard AI – NBA Accreditation Knowledge Base
Source: EvidenceGuard AI - NBA Knowledge Base PDF (IBM AICTE Agentic AI Project)
NBA Manual: May 2026 Edition (GAPC v4.0)
"""

NBA_CHUNKS = [
    {
        "id": "intro_01",
        "section": "Section 1 – Introduction to NBA Accreditation",
        "title": "What is the National Board of Accreditation (NBA)?",
        "content": (
            "The National Board of Accreditation (NBA) is an autonomous accreditation body in India "
            "established under the All India Council for Technical Education (AICTE) Act in 1994, which "
            "later became an independent autonomous body in 2010. NBA evaluates and accredits specific "
            "technical programs (Engineering, Technology, Pharmacy, Architecture, Management, MCA) offered "
            "by higher educational institutions. The primary objective of NBA accreditation is to assess "
            "and enhance the quality of technical education. It fosters Outcome-Based Education (OBE), "
            "ensuring that graduating students possess Graduate Attributes (GAs) aligned with global "
            "professional engineering standards."
        ),
        "source": "Section 1.1 – Introduction | EvidenceGuard AI Knowledge Base",
        "criteria": "General"
    },
    {
        "id": "intro_02",
        "section": "Section 1 – Introduction to NBA Accreditation",
        "title": "Benefits of NBA Accreditation",
        "content": (
            "For Students: NBA accreditation facilitates global mobility, credit transfer, and recognition "
            "of degrees in Washington Accord signatory countries (USA, UK, Australia, Canada, Japan, etc.). "
            "For Institutions: Enhances academic reputation, qualifies the institute for central research "
            "funding (AICTE/DST/SERB grants), and enables autonomous status eligibility. NBA is a full "
            "signatory to the Washington Accord for Tier-I UG Engineering programs."
        ),
        "source": "Section 1.4 – Benefits | EvidenceGuard AI Knowledge Base",
        "criteria": "General"
    },
    {
        "id": "intro_03",
        "section": "Section 1 – NBA vs NAAC Comparison",
        "title": "NBA vs NAAC Differences",
        "content": (
            "NBA focuses on Program-Specific accreditation (e.g., B.Tech in CSE, B.Tech in ECE) and covers "
            "Technical and Professional Education Programs only. NBA uses Outcome-Based Education (OBE) and "
            "GAPC v4.0 methodology and is a full signatory to the Washington Accord for Tier-I UG Engineering. "
            "NAAC, by contrast, is Institutional-Level, covers General Higher Education (Arts, Science, "
            "Commerce), uses Input-Process-Output Quality methodology, and provides Domestic Recognition only."
        ),
        "source": "Section 1.3 – NBA vs NAAC | EvidenceGuard AI Knowledge Base",
        "criteria": "General"
    },
    {
        "id": "tier_01",
        "section": "Section 2 – NBA Accreditation Framework & Tier Classification",
        "title": "Tier-I vs Tier-II Institutions",
        "content": (
            "Tier-I Institutions include IITs, NITs, IIITs, University Faculties/Departments, and Autonomous "
            "Colleges. Tier-I institutions possess academic freedom to design, revise, and execute their own "
            "curriculum and examination system. Evaluation uses grade-based per-criterion assessments "
            "(Y / C / W / D). "
            "Tier-II Institutions are non-autonomous colleges affiliated with a State or Central University. "
            "Tier-II institutions follow the syllabus, examination structure, and evaluation schedule "
            "prescribed by their affiliating university. Evaluation uses direct mark-based scoring out of "
            "1000 points."
        ),
        "source": "Section 2.1 – Tier Classification | EvidenceGuard AI Knowledge Base",
        "criteria": "General"
    },
    {
        "id": "tier_02",
        "section": "Section 2 – Program Eligibility Requirements",
        "title": "Eligibility Requirements for NBA Accreditation",
        "content": (
            "Graduating Batches: Must have at least two graduating student batches prior to the academic year "
            "of application. Continuity: Program must have run uninterrupted for the full standard duration "
            "(e.g., 5 continuous academic years for UG Engineering). Mode of Delivery: Regular full-time "
            "campus programs only. Part-time or distance-learning modes are strictly ineligible. Approval "
            "Status: Must possess valid annual AICTE approval or statutory body sanction for the entire "
            "evaluation window. Student Intake (SFR): Student-Faculty Ratio (SFR) must be maintained at "
            "<=1:25 across the 3 evaluated CAYs to be eligible for 3-year accreditation, and <=1:15 or "
            "1:20 for 6-year status."
        ),
        "source": "Section 2.2 – Eligibility | EvidenceGuard AI Knowledge Base",
        "criteria": "General"
    },
    {
        "id": "tier_03",
        "section": "Section 2 – Accreditation Stages and Evaluation Workflow",
        "title": "NBA Accreditation Process – 4 Phases",
        "content": (
            "Phase 1 – Submission of Pre-Qualifiers (PQ): Institution submits online PQ on the eNBA portal "
            "along with 10% of the accreditation fee. Verifies minimum eligibility (SFR, Admissions %, "
            "Ph.D. faculty ratio). "
            "Phase 2 – SAR Upload: Upon PQ approval, institution pays remaining 90% fee and submits the "
            "detailed SAR within 60 days. "
            "Phase 3 – Peer Team On-Site Evaluation: A 2-to-3 day physical evaluation conducted by a "
            "3-member expert team (1 Chairman + 2 Domain Experts per program). "
            "Phase 4 – EAC Recommendation and NBA Decision: EAC reviews expert reports and conveys final "
            "status (Accredited for 6 Years / Accredited for 3 Years / Not Accredited). "
            "Validity Commencement Rule: Accreditation validity officially begins on January 1st of the "
            "calendar year corresponding to the CAY evaluated during the visit."
        ),
        "source": "Section 2.3 – Evaluation Workflow | EvidenceGuard AI Knowledge Base",
        "criteria": "General"
    },
    {
        "id": "criteria_overview",
        "section": "Section 3 – NBA Accreditation Criteria",
        "title": "NBA 10-Criteria Point Distribution (1000 Marks)",
        "content": (
            "The NBA SAR comprises 10 criteria totaling 1000 marks. Criteria 1–7 assess Programme-Level "
            "operations; Criteria 8–10 assess Institution-Level support. "
            "Criterion 1 – Vision, Mission, and PEOs: 50 Marks (both Tier-I and Tier-II). "
            "Criterion 2 – Curriculum and Teaching-Learning Processes: 100 Marks (Tier-I), 120 Marks (Tier-II). "
            "Criterion 3 – Course Outcomes (COs) and Program Outcomes (POs): 175 Marks (Tier-I), 120 Marks (Tier-II). "
            "Criterion 4 – Students' Performance Evaluation: 100 Marks (Tier-I), 150 Marks (Tier-II). "
            "Criterion 5 – Faculty Information and Contributions: 200 Marks (both tiers). "
            "Criterion 6 – Facilities and Technical Support: 80 Marks (both tiers). "
            "Criterion 7 – Continuous Improvement (CQI): 75 Marks (Tier-I), 50 Marks (Tier-II). "
            "Criterion 8 – First Year Academics (Institute Level): 50 Marks (both tiers). "
            "Criterion 9 – Student Support Systems (Institute Level): 50 Marks (both tiers). "
            "Criterion 10 – Governance, Institutional Support & Financial Resources: 120 Marks (both tiers)."
        ),
        "source": "Section 3.1 – Criteria Distribution | EvidenceGuard AI Knowledge Base",
        "criteria": "All Criteria"
    },
    {
        "id": "crit1_docs",
        "section": "Section 5 – Criterion-Wise Evidence Mapping",
        "title": "Criterion 1 – Vision, Mission & PEOs: Required Documents",
        "content": (
            "Criterion 1 is worth 50 marks for both Tier-I and Tier-II. Required documents: "
            "(1) Institute and Department Vision/Mission statements – evidence format: Signed DAB minutes, "
            "website screenshots, corridor display photos, course file inserts. Custodian: Head of Department (HoD) "
            "and NBA Coordinator. Common Audit Mistake: Vision/Mission statements on website do not match "
            "printed course files. "
            "(2) PEO Dissemination and Process records – evidence format: Stakeholder consultation logs "
            "(Industry, Alumni, Parents, Faculty). Custodian: Program Assessment Committee (PAC). Common Audit "
            "Mistake: Lack of documented proof showing stakeholder involvement in PEO drafting."
        ),
        "source": "Section 5 – Criterion 1 Evidence | EvidenceGuard AI Knowledge Base",
        "criteria": "Criterion 1"
    },
    {
        "id": "crit2_docs",
        "section": "Section 5 – Criterion-Wise Evidence Mapping",
        "title": "Criterion 2 – Curriculum & Teaching-Learning: Required Documents",
        "content": (
            "Criterion 2 is worth 100 marks (Tier-I) or 120 marks (Tier-II). Required documents: "
            "(1) Instructional Delivery and ICT Usage logs – evidence format: LMS usage logs, NPTEL "
            "certificates, smart classroom booking registers. Custodian: Course Coordinators / Module "
            "Coordinators. Common Audit Mistake: Claiming innovative teaching methods without student "
            "evaluation samples. "
            "(2) Project Evaluation Rubrics and Quality – evidence format: Rubric sheets signed by "
            "internal/external guides, project evaluation logs. Custodian: Project Coordinator. Common Audit "
            "Mistake: Identical high marks awarded to all project groups without rubric justification."
        ),
        "source": "Section 5 – Criterion 2 Evidence | EvidenceGuard AI Knowledge Base",
        "criteria": "Criterion 2"
    },
    {
        "id": "crit3_docs",
        "section": "Section 5 – Criterion 3 CO-PO",
        "title": "Criterion 3 – CO-PO Mapping & Attainment",
        "content": (
            "Criterion 3 is worth 175 marks (Tier-I) or 120 marks (Tier-II). It is weighted much higher "
            "in Tier-I due to autonomous control over direct evaluation and complex problem solving. "
            "Required: CO statements for every course, CO-PO mapping matrix using 0/1/2/3 scale, "
            "attainment calculation records showing both direct (80%) and indirect (20%) attainment. "
            "Action Taken Reports (ATR) when CO/PO targets are not met. All 11 POs under GAPC v4.0 must "
            "be mapped. PSOs (2 to 4) must also be included."
        ),
        "source": "Section 3.2 and Section 7 | EvidenceGuard AI Knowledge Base",
        "criteria": "Criterion 3"
    },
    {
        "id": "crit4_docs",
        "section": "Section 5 – Criterion 4 Student Performance",
        "title": "Criterion 4 – Students' Performance Evaluation",
        "content": (
            "Criterion 4 is worth 100 marks (Tier-I) or 150 marks (Tier-II). It is weighted higher in "
            "Tier-II because university exam performance serves as the standardized evaluation metric. "
            "Required documents: Student enrollment data for CAY, CAYm1, CAYm2. Sanctioned intake and "
            "actual admitted student counts must match institute central admission registers. Pass rate data, "
            "academic performance charts, placement records with offer letters."
        ),
        "source": "Section 3.2 and Section 6.2 | EvidenceGuard AI Knowledge Base",
        "criteria": "Criterion 4"
    },
    {
        "id": "crit5_docs",
        "section": "Section 5 – Criterion-Wise Evidence Mapping",
        "title": "Criterion 5 – Faculty Information & Contributions: Required Documents",
        "content": (
            "Criterion 5 is worth 200 marks for both Tier-I and Tier-II. Required documents: "
            "(1) Student-Faculty Ratio (SFR) and Cadre Ratio logs – evidence format: Form-16, salary slips, "
            "AICTE appointment orders, joining reports. Custodian: HoD and Central Establishment Section. "
            "Common Audit Mistake: Counting faculty who joined after November 30th of the CAY in SFR. "
            "(2) Research Publications and Patents – evidence format: Scopus/SCI indexing pages, patent "
            "publication/grant certificates. Custodian: Departmental Research Coordinator. Common Audit "
            "Mistake: Listing papers published in non-indexed or predatory journals (not counted). "
            "Only SCI/SCIE or Scopus-indexed journal papers are counted."
        ),
        "source": "Section 5 – Criterion 5 Evidence | EvidenceGuard AI Knowledge Base",
        "criteria": "Criterion 5"
    },
    {
        "id": "crit6_docs",
        "section": "Section 4 – Documentation Checklist",
        "title": "Criterion 6 – Facilities and Technical Support",
        "content": (
            "Criterion 6 is worth 80 marks for both Tier-I and Tier-II. Required documents: "
            "Laboratory Manuals and Stock Registers: Lab manuals with COs, stock registers, equipment "
            "calibration logs. Major and Minor Project Reports: Project allocation lists, rubrics, evaluation "
            "sheets, sample project reports. Industrial Training and Internship Records: Completion "
            "certificates, student logbooks, feedback forms. Lab Safety compliance: First-aid kits present, "
            "fire extinguishers serviced, lab manuals displaying COs at each setup."
        ),
        "source": "Section 4.3 and Section 8.2 | EvidenceGuard AI Knowledge Base",
        "criteria": "Criterion 6"
    },
    {
        "id": "crit7_docs",
        "section": "Section 4 – Criterion 7 CQI",
        "title": "Criterion 7 – Continuous Quality Improvement (CQI)",
        "content": (
            "Criterion 7 is worth 75 marks (Tier-I) or 50 marks (Tier-II). Lack of Action Taken Reports "
            "(ATR) results in drastic mark deduction in Criterion 7. Required documents: Indirect Feedback "
            "Forms: Course exit surveys, graduate exit surveys, alumni and employer feedback logs. Action "
            "Taken Reports (ATR): Continuous improvement ATRs executed based on CO-PO attainment gaps. "
            "DAB and PAC Meeting Minutes: Signed minutes showing improvement decisions and follow-up."
        ),
        "source": "Section 4.4 and Section 9 | EvidenceGuard AI Knowledge Base",
        "criteria": "Criterion 7"
    },
    {
        "id": "crit8_10",
        "section": "Section 3 – Criteria 8, 9, 10",
        "title": "Criteria 8, 9, 10 – Institute-Level Criteria",
        "content": (
            "Criterion 8 – First Year Academics (Institute Level): 50 marks (both tiers). Covers first-year "
            "teaching SFR, anti-ragging compliance, and first-year student support. "
            "Criterion 9 – Student Support Systems (Institute Level): 50 marks (both tiers). Covers "
            "placement support, scholarships, mentoring, grievance redressal. "
            "Criterion 10 – Governance, Institutional Support and Financial Resources: 120 marks (both tiers). "
            "Capital and operational expenditures reported in Criterion 10 must match audited financial "
            "balance sheets. Financial figures must be consistent across the SAR."
        ),
        "source": "Section 3.1 and Section 6.2 | EvidenceGuard AI Knowledge Base",
        "criteria": "Criterion 8,9,10"
    },
    {
        "id": "checklist_01",
        "section": "Section 4 – Complete NBA Documentation Checklist",
        "title": "Academic and Course Delivery Files Checklist",
        "content": (
            "Faculty and NBA Coordinators must maintain the following across 3 evaluated CAYs (CAY, CAYm1, CAYm2): "
            "1. Institutional Academic Calendar: Approved calendar showing working days, exam slots, and events. "
            "2. Departmental Master Timetable: Class timetables, lab schedules, individual faculty workload logs. "
            "3. Comprehensive Course Files: Syllabus, CO statements, CO-PO mapping matrix, lesson plan, lecture notes. "
            "4. Attendance and Continuous Evaluation Registers: Monthly attendance records, internal assessment marks. "
            "5. Internal Test Question Papers and Answer Schemes: Sample answer scripts (Best, Average, Poor) "
            "with Bloom's taxonomy mapping."
        ),
        "source": "Section 4.1 – Academic Files | EvidenceGuard AI Knowledge Base",
        "criteria": "Criterion 2,3,4"
    },
    {
        "id": "checklist_02",
        "section": "Section 4 – Faculty and Research Dossiers",
        "title": "Faculty and Research Documentation Checklist",
        "content": (
            "1. Faculty Qualification and Service Files: AICTE appointment letters, joining reports, Ph.D. "
            "degrees, bio-data. "
            "2. Research Publications Log: First-page copies of SCI/Scopus indexed journal papers and "
            "conference proceedings. "
            "3. FDP and STTP Training Certificates: Proof of minimum 5-day continuous FDP participation by "
            "faculty members. "
            "4. Consultancy and Funded Project Proofs: Sanction letters, utilization certificates, project "
            "completion reports."
        ),
        "source": "Section 4.2 – Faculty Dossiers | EvidenceGuard AI Knowledge Base",
        "criteria": "Criterion 5"
    },
    {
        "id": "sar_guide",
        "section": "Section 6 – SAR Preparation Guide",
        "title": "SAR Authoring Workflow and Consistency Rules",
        "content": (
            "Step-by-Step SAR Authoring: 1. Form 10 criterion-specific sub-committees under NBA Coordinator "
            "and HoD. 2. Collect accurate academic, student, and faculty data for CAY, CAYm1, CAYm2. "
            "3. Cross-verify: Student enrollment figures, faculty counts, and financial budget figures must be "
            "identical across all 10 criteria. 4. Populate standard eNBA SAR tables without modifying column "
            "headers or formatting. 5. Conduct mock peer visits using internal auditing teams. "
            "Critical Consistency Checkpoints: Faculty headcount in Criterion 5 must match Criterion 3 and 8. "
            "Student enrollment in Criterion 4 must match institute central admission registers. "
            "Financial figures in Criterion 10 must match audited financial balance sheets."
        ),
        "source": "Section 6 – SAR Preparation | EvidenceGuard AI Knowledge Base",
        "criteria": "General – SAR"
    },
    {
        "id": "copomap_01",
        "section": "Section 7 – CO-PO Mapping and Attainment Guide",
        "title": "GAPC v4.0 Standard 11 Program Outcomes (POs)",
        "content": (
            "Under GAPC v4.0 (effective May 2026), 11 POs replace the legacy 12 PO structure: "
            "PO1 – Engineering Knowledge: Apply mathematics, science, engineering fundamentals, and "
            "specialization to solve complex engineering problems. "
            "PO2 – Problem Analysis: Identify, formulate, research literature, and analyze complex engineering "
            "problems reaching substantiated conclusions. "
            "PO3 – Design / Development: Design solutions for complex problems incorporating health, safety, "
            "societal, cultural, and environmental sustainability. "
            "PO4 – Investigations: Conduct investigations of complex problems using research-based knowledge "
            "and synthesis of information. "
            "PO5 – Modern Tool Usage: Create, select, and apply appropriate techniques, resources, and "
            "modern IT/engineering tools. "
            "PO6 – Engineer and the World: Analyze societal, health, safety, legal, and cultural issues "
            "relevant to professional engineering practice. "
            "PO7 – Ethics and Responsibility: Apply ethical principles and commit to professional ethics, "
            "human values, and diversity. "
            "PO8 – Individual and Teamwork: Function effectively as individual and as member or leader in "
            "diverse and multidisciplinary teams. "
            "PO9 – Communication: Communicate effectively on complex engineering activities. "
            "PO10 – Project Management: Demonstrate knowledge and understanding of engineering management "
            "principles applied to projects. "
            "PO11 – Life-long Learning: Recognize the need for, and engage in independent and life-long "
            "learning in technological change."
        ),
        "source": "Section 7.1 – GAPC v4.0 POs | EvidenceGuard AI Knowledge Base",
        "criteria": "Criterion 3"
    },
    {
        "id": "copomap_02",
        "section": "Section 7 – CO-PO Attainment Calculation",
        "title": "CO-PO Mapping Scale and Attainment Formula",
        "content": (
            "CO-PO mapping correlations use a 4-level numerical scale: 0 or Blank = No Correlation, "
            "1 = Slight/Low Correlation, 2 = Moderate/Medium Correlation, 3 = Substantial/High Correlation. "
            "Attainment Formula: Total CO Attainment = (80% x Direct CO Attainment) + (20% x Indirect CO "
            "Exit Survey). "
            "PO Attainment for PO_j = Sum of [CO_i Attainment x Mapping Level of CO_i to PO_j] / "
            "Sum of [Mapping Levels of CO_i to PO_j]. "
            "Illustrative Example: Course Data Structures (CS302). Direct Attainment = 2.40 (80%), Indirect "
            "Exit Survey = 2.80 (20%). Total = (0.80 x 2.40) + (0.20 x 2.80) = 1.92 + 0.56 = 2.48 out of 3.00."
        ),
        "source": "Section 7.2–7.3 – Attainment Formula | EvidenceGuard AI Knowledge Base",
        "criteria": "Criterion 3"
    },
    {
        "id": "gap_analysis",
        "section": "Section 6 – Evidence Gap Identification",
        "title": "How to Identify Missing Evidence in NBA Documentation",
        "content": (
            "Evidence gap identification uses a 3-Tier Verification Model: "
            "Tier 1 – Exists Verification: Confirm the document is physically present in the department record room. "
            "Check: Is the course file present? Is the lab stock register signed? Is the faculty appointment order on file? "
            "Tier 2 – Completeness Verification: Verify all required fields are filled. Check: Does the CO-PO matrix have all 11 POs filled? "
            "Are all test question papers Bloom's taxonomy mapped? Are all faculty designation columns populated? "
            "Tier 3 – Accuracy Verification: Cross-check numbers and data against the SAR tables. "
            "Check: Do faculty counts match across Criteria 3, 5, and 8? Do student enrollment figures match admission registers? "
            "Do financial figures match audited balance sheets? "
            "Common Missing Evidence: Action Taken Reports (ATR) when CO/PO targets missed; "
            "Stakeholder consultation logs for PEO revision; Industry feedback forms for CQI; "
            "Offer letters for all claimed placed students; Calibration logs for lab equipment; "
            "FDP certificates with minimum 5-day duration confirmation."
        ),
        "source": "Section 6.3 – Gap Analysis | EvidenceGuard AI Knowledge Base",
        "criteria": "General – Audit"
    },
    {
        "id": "audit_01",
        "section": "Section 8 – Internal Audit and Compliance Protocols",
        "title": "Departmental Audit Execution Workflow",
        "content": (
            "1. Audit Notification: IQAC issues audit schedules 30 days prior to mock visits. "
            "2. Physical Verification: Internal auditors inspect 100% of course files, laboratory stock "
            "registers, and faculty research dossiers. "
            "3. Gap Logging: Auditors log non-compliances as Deficiency (D), Weakness (W), or Concern (C). "
            "4. Corrective Action Plan (CAP): HoD and PAC execute corrective actions within 15 calendar days. "
            "Audit Checklist: Course File Integrity – random sampling of 5 course files per semester; "
            "all 5 must contain signed syllabus, CO-PO matrix, Bloom's mapped tests, and sample scripts. "
            "Lab Safety and Manuals – first-aid kits present, fire extinguishers serviced, lab manuals "
            "displaying COs. Placement Claims – 100% of claimed placed students must have official company "
            "offer letters on file."
        ),
        "source": "Section 8 – Audit Protocols | EvidenceGuard AI Knowledge Base",
        "criteria": "General – Audit"
    },
    {
        "id": "errors_01",
        "section": "Section 9 – Common NBA Accreditation Errors",
        "title": "Common NBA Errors and How to Prevent Them",
        "content": (
            "1. Inconsistent Faculty List in SAR: Impact – Loss of marks in Criterion 5; possible rejection of "
            "Pre-Qualifier. Prevention – Maintain a central faculty master register cross-checked with Form-16 "
            "and AICTE portal records. "
            "2. Identical CO Attainment Targets: Impact – Visiting team marks Criterion 3 as Weakness (W). "
            "Prevention – Set course-specific target levels based on historical prerequisite performance rather "
            "than a blanket 60%. "
            "3. Lack of Action Taken Reports (ATR): Impact – Drastic mark deduction in Criterion 7 (CQI). "
            "Prevention – Ensure PAC signed ATRs exist showing explicit actions taken when CO/PO attainment "
            "targets are missed."
        ),
        "source": "Section 9 – Common Errors | EvidenceGuard AI Knowledge Base",
        "criteria": "General"
    },
    {
        "id": "glossary_01",
        "section": "Section 10 – Glossary",
        "title": "NBA Terminology and Abbreviations",
        "content": (
            "SAR – Self-Assessment Report: Primary document compiled by institution detailing compliance with "
            "NBA's 10 criteria. "
            "OBE – Outcome-Based Education: Educational theory focusing on goals (outcomes). "
            "GAPC v4.0 – Graduate Attributes and Professional Competencies v4.0: International benchmark "
            "framework updated by Washington Accord in 2021. "
            "PEO – Program Educational Objectives: Broad statements describing career and professional "
            "accomplishments expected 3–5 years after graduation. "
            "PO – Program Outcomes: 11 statements (GAPC v4.0) describing what students are expected to know "
            "and be able to do upon graduation. "
            "CO – Course Outcomes: Clear statements of key abilities a student is expected to demonstrate at "
            "conclusion of a specific course. "
            "PSO – Program Specific Outcomes: Statements specific to a particular engineering discipline "
            "defined by the institution (typically 2 to 4 PSOs). "
            "SFR – Student-Faculty Ratio: Ratio of total enrolled students across all years to full-time "
            "dedicated regular faculty members. "
            "CAY / CAYm1 – Current Academic Year / CAY Minus 1: Evaluation base years assessed during visit. "
            "DAB / PAC – Departmental Advisory Board / Program Assessment Committee: Committees overseeing "
            "accreditation governance and CQI."
        ),
        "source": "Section 10 – Glossary | EvidenceGuard AI Knowledge Base",
        "criteria": "General"
    },
    {
        "id": "faq_01",
        "section": "Section 11 – Practical Faculty FAQs",
        "title": "FAQ: SFR, Ph.D., FDP, and Publication Requirements",
        "content": (
            "Q1: Maximum SFR for 6-year accreditation? For 6-year accreditation, the SFR must be <=1:15 "
            "across evaluated CAYs. SFR between 1:15.1 and 1:20 qualifies for maximum 3-year accreditation. "
            "(Source: SAR Criterion 5 Manual) "
            "Q2: Can adjunct/visiting faculty be counted in SFR? Adjunct/visiting faculty can contribute a "
            "maximum of 10% towards total required faculty strength, provided they conduct at least 50% of a "
            "full course load. (Source: NBA Faculty Guidelines) "
            "Q4: Minimum Ph.D. faculty requirement? At least 30% of regular required faculty members must "
            "hold a Ph.D. degree for 6-year accreditation status. (Source: SAR Criterion 5) "
            "Q5: Are non-Scopus journal papers counted? No. Points awarded exclusively for SCI/SCIE or "
            "Scopus-indexed journals. (Source: SAR Criterion 5 Evaluation) "
            "Q6: Minimum FDP duration? An FDP must be at least 5 consecutive working days to be counted as "
            "full faculty development credit. (Source: SAR Criterion 5)"
        ),
        "source": "Section 11 – FAQ Q1–Q6 | EvidenceGuard AI Knowledge Base",
        "criteria": "Criterion 5"
    },
    {
        "id": "faq_02",
        "section": "Section 11 – Practical Faculty FAQs",
        "title": "FAQ: POs, Attainment, Tier Evaluation, Visit Procedures",
        "content": (
            "Q3: How many POs must be mapped? Exactly 11 POs must be mapped under GAPC v4.0 framework "
            "(May 2026 edition onwards). (Source: Section 3 GAPC v4.0) "
            "Q7: Weightage split between direct and indirect attainment? 80% Direct (internal tests, "
            "assignments, university exams) and 20% Indirect (course exit surveys). "
            "(Source: Section 7 Attainment Guide) "
            "Q8: Does Tier-II use grade markers or numeric marks? Tier-II uses absolute numeric marks totaling "
            "1000 points. Tier-I uses grade markers (Y / C / W / D). (Source: Section 2.1) "
            "Q9: How many dates must institution propose for peer team visit? 5 sets of visit dates "
            "(maximum 2 sets per month) during active regular teaching days on eNBA portal. "
            "Q10: Can a program withdraw from accreditation during the visit? Yes, formally during the Exit "
            "Meeting by handing a written request signed by Head of Institution to the Team Chair. "
            "Q11: Fee penalty for postponing visit after expert team constitution? A 25% fee deduction "
            "penalty applies if postponement is requested after team constitution and travel bookings."
        ),
        "source": "Section 11 – FAQ Q3, Q7–Q11 | EvidenceGuard AI Knowledge Base",
        "criteria": "General"
    },
]
