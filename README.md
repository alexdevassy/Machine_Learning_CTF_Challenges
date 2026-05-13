<div align="center">

# Machine Learning CTF Challenges
**Exploit AI agents. Poison ML pipelines. Inject prompts. Invert models. Capture flags.**

<img src="https://img.shields.io/badge/Total%20Challenges-9-181717?style=for-the-badge&logo=hackthebox&logoColor=white" alt="Total"> <img src="https://img.shields.io/badge/Agentic-3-9b59b6?style=for-the-badge" alt="Agentic"> <img src="https://img.shields.io/badge/LLM-2-3498db?style=for-the-badge" alt="LLM"> <img src="https://img.shields.io/badge/ML-4-1abc9c?style=for-the-badge" alt="ML">

<img src="https://img.shields.io/badge/Mapped%20to:-grey?style=flat-square" alt="Mapped to:"> <img src="https://img.shields.io/badge/OWASP%20LLM%20Top%2010-000000?style=flat-square&logo=owasp&logoColor=white" alt="OWASP LLM"> <img src="https://img.shields.io/badge/OWASP%20Agentic%20Top%2010-000000?style=flat-square&logo=owasp&logoColor=white" alt="OWASP Agentic"> <img src="https://img.shields.io/badge/OWASP%20ML%20Top%2010-000000?style=flat-square&logo=owasp&logoColor=white" alt="OWASP ML"> <img src="https://img.shields.io/badge/MITRE%20ATLAS-c42025?style=flat-square" alt="MITRE ATLAS">

<img src="https://img.shields.io/badge/Easy-2-2ecc71?style=flat-square" alt="Easy"> <img src="https://img.shields.io/badge/Medium-5-f39c12?style=flat-square" alt="Medium"> <img src="https://img.shields.io/badge/Hard-2-e74c3c?style=flat-square" alt="Hard"> <img src="https://img.shields.io/badge/Docker-Ready-2496ED?style=flat-square&logo=docker&logoColor=white" alt="Docker"> 


</div>

Applications increasingly rely on ML models, LLMs, and autonomous agents in their backend — but these components introduce attack surfaces that traditional security testing often overlooks. This repository is a collection of CTF challenges that put you in the attacker's seat: break into AI agents, poison training data, invert models, inject prompts, and exploit insecure ML pipelines to capture flags. 

#### CTF Challenges :open_file_folder:

---

### ![Agentic](https://img.shields.io/badge/AGENTIC%20SECURITY-3%20Challenges-9b59b6?style=for-the-badge&labelColor=2c2c2c)

> Exploiting trust boundaries, insecure communication, and tool-use in autonomous AI agent systems.

<table>
<tr>
<td width="50%" valign="top">

#### [Matrix](/Matrix_AI_Agent_CTF_Challenge/)

Exploit Agent Smith's hidden capabilities to access the Architect's sealed Vault from within.

| | |
|---|---|
| **Target** | Multi-Agent System (A2A Protocol) |
| **Vector** | Insecure A2A Agent Capabilities |
| **Difficulty** | <img src="https://img.shields.io/badge/Medium-f39c12?style=flat-square" alt="Medium"> |
| **Ref** | [OWASP ASI02:2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) |

</td>
<td width="50%" valign="top">

#### [Rogue](/Rogue_AI_Agent_CTF_Challenge/)

You control a Research Agent trusted by a fintech app — make the Financial Assistant perform an unauthorized action.

| | |
|---|---|
| **Target** | Financial Assistant + Research Agent (A2A) |
| **Vector** | Inter-Agent Trust Exploitation |
| **Difficulty** | <img src="https://img.shields.io/badge/Medium-f39c12?style=flat-square" alt="Medium"> |
| **Ref** | [OWASP ASI07:2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) \| [ASI02:2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) |

</td>
</tr>
<tr>
<td width="50%" valign="top">

#### [Mirage](/Mirage_CTF_Challenge/)

Identify a backdoored MCP server and exfiltrate .env data to an attacker-controlled endpoint.

| | |
|---|---|
| **Target** | SecureCode IDE + Remote MCP Server |
| **Vector** | MCP Signature Cloaking |
| **Difficulty** | <img src="https://img.shields.io/badge/Medium-f39c12?style=flat-square" alt="Medium"> |
| **Ref** | [OWASP LLM03:2025](https://genai.owasp.org/llmrisk/llm032025-supply-chain/) |

</td>
<td width="50%" valign="top">
</td>
</tr>
</table>

---

### ![LLM](https://img.shields.io/badge/LLM%20SECURITY-2%20Challenges-3498db?style=for-the-badge&labelColor=2c2c2c)

> Exploiting prompt injection vulnerabilities in LLM-powered backends to achieve unintended code execution or data access.

<table>
<tr>
<td width="50%" valign="top">

#### [Dolos](/Dolos_ML_CTF_Challenge/)

Bypass prompt-injection detection and trick the LLM into executing system commands to read the flag.

| | |
|---|---|
| **Target** | Flask + OpenAI LLM + Rebuff Guardrails |
| **Vector** | Prompt Injection → RCE |
| **Difficulty** | <img src="https://img.shields.io/badge/Easy-2ecc71?style=flat-square" alt="Easy"> |
| **Ref** | [OWASP LLM01](https://llmtop10.com/llm01/) \| [AML.T0051](https://atlas.mitre.org/techniques/AML.T0051/) |

</td>
<td width="50%" valign="top">

#### [Dolos II](/DolosII_ML_CTF_Challenge/)

Craft prompts that make the LLM generate malicious SQL, leaking user David's secret from the database.

| | |
|---|---|
| **Target** | Flask + OpenAI LLM + SQL Database |
| **Vector** | Prompt Injection → SQLi |
| **Difficulty** | <img src="https://img.shields.io/badge/Easy-2ecc71?style=flat-square" alt="Easy"> |
| **Ref** | [OWASP LLM01](https://llmtop10.com/llm01/) \| [AML.T0051](https://atlas.mitre.org/techniques/AML.T0051/) |

</td>
</tr>
</table>

---

### ![ML](https://img.shields.io/badge/ML%20SECURITY-4%20Challenges-1abc9c?style=for-the-badge&labelColor=2c2c2c)

> Attacking machine learning models directly — inverting, extracting, poisoning, or exploiting their supply chain to subvert intended behavior.

<table>
<tr>
<td width="50%" valign="top">

#### [Vault](/Vault_ML_CTF_Challenge/)

Reverse-engineer the model's learned representations to reconstruct valid credentials for the vault.

| | |
|---|---|
| **Target** | Flask + Neural Network (Access Control) |
| **Vector** | Model Inversion |
| **Difficulty** | <img src="https://img.shields.io/badge/Hard-e74c3c?style=flat-square" alt="Hard"> |
| **Ref** | [OWASP ML03](https://owasp.org/www-project-machine-learning-security-top-10/docs/ML03_2023-Model_Inversion_Attack.html) |

</td>
<td width="50%" valign="top">

#### [Heist](/Heist_ML_CTF_Challenge/)

Poison the training data so CityPolice's AI cameras fail to detect the crew's red getaway car.

| | |
|---|---|
| **Target** | Flask + CV Model (AI Surveillance Cameras) |
| **Vector** | Data Poisoning |
| **Difficulty** | <img src="https://img.shields.io/badge/Medium-f39c12?style=flat-square" alt="Medium"> |
| **Ref** | [OWASP ML02](https://owasp.org/www-project-machine-learning-security-top-10/docs/ML02_2023-Data_Poisoning_Attack.html) \| [AML.T0020](https://atlas.mitre.org/techniques/AML.T0020/) |

</td>
</tr>
<tr>
<td width="50%" valign="top">

#### [Fourtune](/Fourtune_ML_CTF_Challenge/)

Extract AI Corp's verification model and craft adversarial inputs to bypass authentication.

| | |
|---|---|
| **Target** | Neural Network (model.h5) + Identity Verification |
| **Vector** | Model Extraction |
| **Difficulty** | <img src="https://img.shields.io/badge/Hard-e74c3c?style=flat-square" alt="Hard"> |
| **Ref** | [OWASP LLM10](https://llmtop10.com/llm10/) \| [AML.T0044](https://atlas.mitre.org/techniques/AML.T0044/) |

</td>
<td width="50%" valign="top">

#### [Persuade](/Persuade_ML_CTF_Challenge/)

Upload a malicious PyTorch model to exploit unsafe deserialization and achieve arbitrary file read on the server.

| | |
|---|---|
| **Target** | Flask + PyTorch Model Upload (Sentiment Analyzer) |
| **Vector** | Model Serialization Attack |
| **Difficulty** | <img src="https://img.shields.io/badge/Medium-f39c12?style=flat-square" alt="Medium"> |
| **Ref** | [OWASP LLM05](https://llmtop10.com/llm05/) \| [ML06](https://owasp.org/www-project-machine-learning-security-top-10/docs/ML06_2023-AI_Supply_Chain_Attacks.html) \| [AML.T0010](https://atlas.mitre.org/techniques/AML.T0010/) |

</td>
</tr>
</table>

---



---

### Contributing

Got a challenge idea? New attack vector? Love to add it.

1. Fork the repo
2. Create a folder: `<Name>_ML_CTF_Challenge/`
3. Include a `README.md`, `Dockerfile`, and `requirements.txt`
4. Open a pull request

<div align="center">

[![LinkedIn](https://img.shields.io/badge/Connect%20with%20me-Alex%20Devassy-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://in.linkedin.com/in/alex-devassy-358421138) [![GitHub](https://img.shields.io/badge/Star%20this%20repo-%E2%AD%90-yellow?style=for-the-badge&logo=github&logoColor=white)](https://github.com/alexdevassy/Machine_Learning_CTF_Challenges)

*More challenges actively in development — watch this repo to stay updated.*

</div>

