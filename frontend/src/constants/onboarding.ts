export const DEPARTMENTS = [
  "Software Engineering & Application Modernization",
  "Cloud Infrastructure & Platforms",
  "Cybersecurity & Digital Identity",
  "Data Analytics, AI & Business Intelligence",
  "Quality Assurance & Test Automation",
  "IT Service Management & Workplace Operations",
  "Digital Consulting & Transformation Advisory",
  "Product Management & UX/UI Design",
  "Enterprise Architecture & Solutions Design",
  "Human Resources & Talent Acquisition",
  "Finance, Legal & Corporate Governance",
  "Sales, Presales & Account Management",
  "Project Management Office (PMO)",
  "Internal IT & Information Security",
  "Marketing & Corporate Communications",
  "Procurement & Supply Chain Management",
] as const;

export const DEPARTMENT_ROLE_MAPPING: Record<string, string[]> = {
  "Software Engineering & Application Modernization": [
    "Junior Frontend Developer", "Frontend Developer", "Senior Frontend Developer",
    "Junior Backend Engineer", "Backend Engineer", "Senior Backend Engineer",
    "Junior Full-Stack Engineer", "Full-Stack Engineer", "Senior Full-Stack Engineer",
    "Lead Software Engineer", "Software Architect",
  ],
  "Cloud Infrastructure & Platforms": [
    "Junior DevOps Engineer", "DevOps Engineer", "Senior DevOps Engineer",
    "Junior Cloud Engineer", "Cloud Solutions Architect", "Site Reliability Engineer (SRE)",
    "Systems Administrator",
  ],
  "Cybersecurity & Digital Identity": [
    "Junior Security Analyst", "SOC Analyst", "Cybersecurity Engineer",
    "Penetration Tester", "IAM Specialist", "GRC Consultant",
  ],
  "Data Analytics, AI & Business Intelligence": [
    "Junior Data Analyst", "Data Analyst", "Junior Data Engineer",
    "Data Engineer", "Senior Data Engineer", "Machine Learning Engineer",
    "AI/ML Research Scientist", "BI Developer",
  ],
  "Quality Assurance & Test Automation": [
    "Junior QA Tester", "QA Automation Engineer", "Senior QA Automation Engineer",
    "Performance Test Specialist", "Test Lead",
  ],
  "IT Service Management & Workplace Operations": [
    "IT Service Desk Specialist (L1/L2)", "Senior Service Desk Engineer (L3)",
    "Incident & Problem Manager", "Service Delivery Manager",
    "Workplace Support Technician", "IT Operations Lead",
  ],
  "Digital Consulting & Transformation Advisory": [
    "Associate Consultant", "Technology Consultant", "Senior Digital Consultant",
    "Consulting Manager", "Solutions Architect",
  ],
  "Product Management & UX/UI Design": [
    "Junior UI/UX Designer", "UI/UX Designer", "Senior Product Designer",
    "Product Owner", "Technical Product Manager",
  ],
  "Enterprise Architecture & Solutions Design": [
    "Associate Solutions Architect", "Enterprise Architect", "Chief Solutions Architect",
    "Domain Architect (Cloud/Data/Security)", "Integration Architect", "Technology Strategy Consultant",
  ],
  "Human Resources & Talent Acquisition": [
    "Talent Acquisition Specialist", "HR Operations Specialist", "HR Business Partner",
    "Learning & Development Specialist", "Compensation & Benefits Analyst",
  ],
  "Finance, Legal & Corporate Governance": [
    "Financial Analyst", "Senior Corporate Accountant", "Legal Counsel / Contract Specialist",
    "Compliance & Regulatory Officer", "Tax & Treasury Specialist", "Financial Controller",
  ],
  "Sales, Presales & Account Management": [
    "Business Development Representative (BDR)", "Account Executive", "Senior Key Account Manager",
    "Presales Solution Consultant", "Bid & Proposal Manager", "Sales Director",
  ],
  "Project Management Office (PMO)": [
    "PMO Analyst", "Scrum Master", "Junior Project Manager",
    "Project Manager", "Senior Project Manager", "Program Director",
  ],
  "Internal IT & Information Security": [
    "Internal Systems Administrator", "Network & Systems Engineer", "Internal IT Support Specialist",
    "Information Security Analyst", "Endpoint Management Specialist", "Internal IT Infrastructure Lead",
  ],
  "Marketing & Corporate Communications": [
    "Content Marketing Specialist", "Digital Marketing Manager", "Corporate Communications Specialist",
    "Brand & Public Relations Manager", "Event & Campaign Coordinator", "Internal Communications Officer",
  ],
  "Procurement & Supply Chain Management": [
    "Procurement Specialist", "IT Vendor Manager", "Sourcing & Contract Specialist",
    "Supply Chain Analyst", "Category Manager (Hardware & Software)", "Purchasing Officer",
  ],
};

export const LOCATION_OPTIONS = ["Romania, Timisoara", "France, Paris", "China, Beijing"];
export const WORK_LOCATION_OPTIONS = ["on-site", "remote", "hybrid"];
export const EMPLOYMENT_TYPE_OPTIONS = ["full-time", "part-time", "contract"];