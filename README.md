# Tuwaiq Auto Mailer
### Modular Club Communications Engine

A highly modular, CLI-driven SMTP mailing utility designed to automate acceptance letters and communications for student organizations (Tuwaiq Club, AWS Club, Cybersecurity Club, etc.).

---

## Architecture

Tuwaiq Auto Mailer is completely identity-agnostic — no hardcoded emails, subjects, or layouts. Club identity is defined entirely through HTML templates and CLI arguments.

---

## Setup

### 1. Environment Variables

Create a `.env` file in the root directory with your sender credentials. Use an **App Password**, not your raw account password.

```env
CLUB_EMAIL=your_club_workspace@ksu.edu.sa
CLUB_EMAIL_PASSWORD=your_16_char_app_password
```

### 2. Install Dependencies

```bash
pip install python-dotenv
```

---

## Usage

Run the mailer from the CLI, providing your target CSV, HTML template, role, subject, and sender name.

### Example — Tuwaiq Club (Members)

```bash
python mailer.py \
  -c "معلومات طويق - الاعضاء.csv" \
  -t "templates/tuwaiq_template.html" \
  -r "عضو" \
  -s "مبارك قبولك في نادي طويق الطلابي!" \
  -n "Tuwaiq Club"
```

### Example — AWS Club (Leaders)

```bash
python mailer.py \
  -c "aws_leaders_sp26.csv" \
  -t "templates/aws_club_template.html" \
  -r "قائد" \
  -s "Welcome to the AWS Club Leadership Team" \
  -n "KSU AWS Club"
```

### Advanced — Custom CSV Headers

If your CSV uses non-default column names (e.g., from a custom Google Form), override them with optional flags:

```bash
python mailer.py \
  -c "custom.csv" \
  -t "template.html" \
  -r "عضو" \
  -s "Welcome" \
  -n "Cyber Club" \
  --name-col "الاسم الثلاثي" \
  --track-col "القسم" \
  --email-col "الايميل الجامعي"
```

---

## Template Variables

HTML templates in `templates/` must include these placeholders:

| Variable | Description |
|----------|-------------|
| `{{NAME}}` | Student's full name |
| `{{TRACK}}` | Department or track |
| `{{ROLE}}` | Assigned role (e.g., `عضو`, `قائد`) |

---

## Project Structure

```
nexusmail/
├── mailer.py
├── .env
└── templates/
    ├── tuwaiq_template.html
    ├── aws_club_template.html
    └── ...
```

---

## Template Preview — `tuwaiq_template.html`

<details>
<summary>View full HTML source</summary>

```html
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>قبول نادي طويق الطلابي</title>
    <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;500;700&display=swap" rel="stylesheet">
</head>
<body style="margin: 0; padding: 0; background-color: #ededed; font-family: 'IBM Plex Sans Arabic', Arial, sans-serif; direction: rtl;">

    <table border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed; background-color: #ededed;">
        <tr>
            <td align="center" style="padding: 40px 10px;">
                
                <table border="0" cellpadding="0" cellspacing="0" width="600" style="background-color: #4f29b7; border-radius: 12px; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.15);">
                    
                    <!-- Header Logos -->
                    <tr>
                        <td style="padding: 30px 40px 10px 40px;">
                            <table border="0" cellpadding="0" cellspacing="0" width="100%">
                                <tr>
                                    <td align="right" width="50%">
                                        <img src="https://raw.githubusercontent.com/YourOrg/YourRepo/main/assets/tuwaiq-logo.png" alt="Tuwaiq Club" style="display: block; max-height: 40px;">
                                    </td>
                                    <td align="left" width="50%">
                                        <img src="https://raw.githubusercontent.com/YourOrg/YourRepo/main/assets/ccis-logo.png" alt="CCIS" style="display: block; max-height: 40px;">
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>

                    <!-- Headline -->
                    <tr>
                        <td align="center" style="padding: 30px 40px 10px 40px;">
                            <h1 style="color: #ffffff; margin: 0; font-size: 28px; font-weight: 700;">
                                نُبارك لك انضمامك معنا !
                            </h1>
                        </td>
                    </tr>

                    <!-- Name -->
                    <tr>
                        <td align="center" style="padding: 10px 40px;">
                            <h2 style="color: #57e3d8; margin: 0; font-size: 24px; font-weight: 700;">
                                {{NAME}}
                            </h2>
                        </td>
                    </tr>

                    <!-- Role & Track -->
                    <tr>
                        <td align="center" style="padding: 10px 40px 30px 40px;">
                            <p style="color: #ededed; margin: 0; font-size: 16px; font-weight: 500;">
                                بمنصب {{ROLE}} في مسار {{TRACK}}
                            </p>
                        </td>
                    </tr>

                    <!-- Traits -->
                    <tr>
                        <td align="center" style="padding: 20px 40px;">
                            <table border="0" cellpadding="0" cellspacing="0" width="100%">
                                <tr>
                                    <td align="center" style="position: relative;">
                                        <div style="border-top: 1px solid #ffffff; width: 85%; margin: 0 auto 25px auto; position: relative;">
                                            <span style="background-color: #4f29b7; color: #ffffff; padding: 0 15px; position: relative; top: -14px; font-size: 18px; font-weight: 700;">
                                                لأنـــــــــــــــــــــك
                                            </span>
                                        </div>
                                    </td>
                                </tr>
                            </table>
                            
                            <table border="0" cellpadding="0" cellspacing="0" width="85%" style="margin: 0 auto; border-spacing: 10px; border-collapse: separate;">
                                <tr>
                                    <td align="center" width="33%" style="border: 1px solid #57e3d8; border-radius: 6px; padding: 8px 0;">
                                        <span style="color: #57e3d8; font-weight: 700; font-size: 15px;">مُبدع</span>
                                    </td>
                                    <td align="center" width="33%" style="border: 1px solid #f4a664; border-radius: 6px; padding: 8px 0;">
                                        <span style="color: #f4a664; font-weight: 700; font-size: 15px;">مُلهم</span>
                                    </td>
                                    <td align="center" width="33%" style="border: 1px solid #a380ff; border-radius: 6px; padding: 8px 0;">
                                        <span style="color: #a380ff; font-weight: 700; font-size: 15px;">طموح</span>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>

                    <!-- Footer -->
                    <tr>
                        <td align="center" style="padding: 40px 40px 20px 40px;">
                            <p style="color: #ffffff; margin: 0; font-size: 18px; font-weight: 500;">
                                مرحبًا بك في نادي طويق الطلابي
                            </p>
                        </td>
                    </tr>

                    <tr>
                        <td align="left" style="padding: 0px 40px 20px 40px;">
                            <p style="color: #ededed; margin: 0; font-size: 12px; font-family: Arial, sans-serif;" dir="ltr">
                                𝕏 in Ⓝ @TuwaiqClub
                            </p>
                        </td>
                    </tr>

                </table>
            </td>
        </tr>
    </table>
</body>
</html>
```

</details>
