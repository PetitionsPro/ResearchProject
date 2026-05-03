# CV Parser API Documentation

This document describes the API exposed by the current Django REST Framework backend.

## Base URL

Local development:

```text
http://127.0.0.1:8000/
```

All endpoint paths below are relative to the base URL.

## Authentication

The API uses JWT bearer authentication through `rest_framework_simplejwt`.

Send authenticated requests with:

```http
Authorization: Bearer <access_token>
```

Token lifetime configured in the current system:

| Token | Lifetime |
| --- | --- |
| Access token | 5 days |
| Refresh token | 7 days |

Some endpoints are public, some require any authenticated user, and some require an admin/staff user. See each endpoint for details.

## Common Responses

| Status | Meaning |
| --- | --- |
| `200 OK` | Request completed successfully. |
| `201 Created` | Resource was created successfully. |
| `400 Bad Request` | Validation failed or required data is missing. |
| `401 Unauthorized` | Authentication failed or credentials are invalid. |
| `403 Forbidden` | The authenticated user does not have permission. |

## Accounts

### Register User

Creates a new user account.

```http
POST /accounts/register/
```

Authentication: public

Content type:

```http
Content-Type: application/json
```

Request body:

```json
{
  "email": "user@example.com",
  "password": "StrongPassword123",
  "confirm_password": "StrongPassword123",
  "full_name": "Example User"
}
```

Fields:

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `email` | string | yes | Must be a valid, unique email address. |
| `password` | string | yes | Saved as a hashed password. |
| `confirm_password` | string | yes | Must match `password`. |
| `full_name` | string | no | User display name. |

Success response:

```http
201 Created
```

```json
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "full_name": "Example User"
  }
}
```

Validation error example:

```http
400 Bad Request
```

```json
{
  "password": "Passwords do not match"
}
```

Example:

```bash
curl -X POST http://127.0.0.1:8000/accounts/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "StrongPassword123",
    "confirm_password": "StrongPassword123",
    "full_name": "Example User"
  }'
```

### Login User

Authenticates a user and returns JWT tokens.

```http
POST /accounts/login/
```

Authentication: public

Content type:

```http
Content-Type: application/json
```

Request body:

```json
{
  "email": "user@example.com",
  "password": "StrongPassword123"
}
```

Success response:

```http
200 OK
```

```json
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "full_name": "Example User"
  },
  "refresh": "<refresh_token>",
  "access": "<access_token>"
}
```

Invalid credentials response:

```http
401 Unauthorized
```

```json
{
  "detail": "Invalid credentials"
}
```

Example:

```bash
curl -X POST http://127.0.0.1:8000/accounts/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "StrongPassword123"
  }'
```

## CV Parsing

### Parse CV

Uploads a PDF resume, extracts candidate data, anonymizes personal information, stores the parsed record, generates a 5-sentence career story with OpenAI, and returns that story.

```http
POST /cv/parse/
```

Authentication: required

Content type:

```http
Content-Type: multipart/form-data
Authorization: Bearer <access_token>
```

Request body:

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `file` | file | yes | Must be a `.pdf` file. |

Success response:

```http
200 OK
```

```json
{
  "story": "Sentence 1. Sentence 2. Sentence 3. Sentence 4. Sentence 5."
}
```

Validation error example:

```http
400 Bad Request
```

```json
{
  "file": [
    "Only PDF files are allowed."
  ]
}
```

Processing behavior:

| Step | Description |
| --- | --- |
| PDF parsing | Text is extracted from every page using `pypdf`. |
| Contact extraction | Emails and phone numbers are extracted with regular expressions. |
| NLP extraction | Skills, experience, education, soft skills, and address-like entities are extracted with the local NLP pipeline. |
| PII storage | Name, email, phone, and address are encrypted before being saved. |
| Blind indexes | Email, phone, and address search indexes are generated with HMAC-SHA256. |
| Story generation | Non-personal resume data is sent to OpenAI using the `gpt-4o-mini` model. |

Example:

```bash
curl -X POST http://127.0.0.1:8000/cv/parse/ \
  -H "Authorization: Bearer <access_token>" \
  -F "file=@/path/to/resume.pdf"
```

### List Story Data

Returns stored parsed CV records.

```http
GET /cv/story-data/
```

Authentication: required

Authorization:

```http
Authorization: Bearer <access_token>
```

Permissions and filtering:

| User type | Result |
| --- | --- |
| Staff/admin user | Returns all parsed records. |
| Normal authenticated user | Returns only records owned by the current user. |

Success response:

```http
200 OK
```

```json
[
  {
    "id": 1,
    "user": 1,
    "name": "<encrypted_name>",
    "email": "<encrypted_email>",
    "email_idx": "<blind_index>",
    "phone": "<encrypted_phone>",
    "phone_idx": "<blind_index>",
    "address": "<encrypted_address>",
    "address_idx": "<blind_index>",
    "skills": "Python, Django, REST API",
    "soft_skills": "Communication, Leadership",
    "story": "Sentence 1. Sentence 2. Sentence 3. Sentence 4. Sentence 5.",
    "experience": "Software Engineer at Example Company",
    "education": "BSc in Computer Science",
    "resume": "/media/resumes/resume.pdf",
    "created_at": "2026-05-03T12:00:00Z",
    "updated_at": "2026-05-03T12:00:00Z"
  }
]
```

Note: the queryset optimizes only `id`, `story`, and `resume`, but the serializer currently exposes all model fields. Accessing other fields may trigger extra database queries.

Example:

```bash
curl http://127.0.0.1:8000/cv/story-data/ \
  -H "Authorization: Bearer <access_token>"
```

### Search Stories and Return Masked Personal Data

Searches candidate stories by text and returns unique masked personal information from matching records.

```http
GET /cv/story/user-data/?search=<query>
```

Authentication: required

Permission: admin/staff user only

Query parameters:

| Parameter | Type | Required | Notes |
| --- | --- | --- | --- |
| `search` | string | no | Matches against `story` using case-insensitive containment. If omitted, all records are searched. |

Success response:

```http
200 OK
```

```json
{
  "email": [
    "u****r@example.com"
  ],
  "phone": [
    "****1234"
  ],
  "address": [
    "Dhaka****esh"
  ]
}
```

Behavior:

| Field | Behavior |
| --- | --- |
| `email` | Decrypted, deduplicated, then masked. |
| `phone` | Decrypted, deduplicated, then masked. |
| `address` | Decrypted, deduplicated, then masked. |
| `name` | Decrypted internally but not returned. |

Example:

```bash
curl "http://127.0.0.1:8000/cv/story/user-data/?search=Django" \
  -H "Authorization: Bearer <admin_access_token>"
```

### Search Story by Exact Email or Phone

Searches parsed CV records by exact email or phone value using the stored blind index. Returns story and resume only.

```http
GET /cv/story/search/?search=<email_or_phone>
```

Authentication: required

Permission: admin/staff user only

Query parameters:

| Parameter | Type | Required | Notes |
| --- | --- | --- | --- |
| `search` | string | yes | Exact email or phone value. The API hashes it with the blind-index key and compares it with stored indexes. |

Success response:

```http
200 OK
```

```json
[
  {
    "id": 1,
    "story": "Sentence 1. Sentence 2. Sentence 3. Sentence 4. Sentence 5.",
    "resume": "/media/resumes/resume.pdf"
  }
]
```

No match response:

```http
200 OK
```

```json
[]
```

Example:

```bash
curl "http://127.0.0.1:8000/cv/story/search/?search=user@example.com" \
  -H "Authorization: Bearer <admin_access_token>"
```

## Dynamic Data

### Bulk Create Skills

Creates multiple skill records.

```http
POST /data/skills/bulk-create/
```

Authentication: not required by the current view

Content type:

```http
Content-Type: application/json
```

Request body:

```json
{
  "bulk_skills": [
    "Python",
    "Django",
    "React"
  ]
}
```

Fields:

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `bulk_skills` | array of strings | yes | Every item must be a string. |

Success response:

```http
201 Created
```

```json
{
  "message": "Skills created successfully"
}
```

Validation error examples:

```http
400 Bad Request
```

```json
{
  "bulk_skills": [
    "bulk_skills must be a list of skill names."
  ]
}
```

```json
{
  "bulk_skills": [
    "Each skill name must be a string."
  ]
}
```

Example:

```bash
curl -X POST http://127.0.0.1:8000/data/skills/bulk-create/ \
  -H "Content-Type: application/json" \
  -d '{
    "bulk_skills": ["Python", "Django", "React"]
  }'
```

### Bulk Create Education

Creates multiple education records.

```http
POST /data/education/bulk-create/
```

Authentication: not required by the current view

Content type:

```http
Content-Type: application/json
```

Request body:

```json
{
  "bulk_education": [
    "Bachelor of Science",
    "Master of Science"
  ]
}
```

Fields:

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `bulk_education` | array of strings | yes | Every item must be a string. |

Success response:

```http
201 Created
```

```json
{
  "message": "Educations created successfully"
}
```

Validation error examples:

```http
400 Bad Request
```

```json
{
  "bulk_education": [
    "bulk_education must be a list of education names."
  ]
}
```

```json
{
  "bulk_education": [
    "Each education name must be a string."
  ]
}
```

Example:

```bash
curl -X POST http://127.0.0.1:8000/data/education/bulk-create/ \
  -H "Content-Type: application/json" \
  -d '{
    "bulk_education": ["Bachelor of Science", "Master of Science"]
  }'
```

## Data Models Returned by the API

### User

| Field | Type | Notes |
| --- | --- | --- |
| `id` | integer | User primary key. |
| `email` | string | Unique login email. |
| `full_name` | string or null | Optional full name. |

### Candidate Parsed Data

| Field | Type | Notes |
| --- | --- | --- |
| `id` | integer | Parsed record primary key. |
| `user` | integer | Owner user ID. |
| `name` | string or null | Encrypted candidate name. Current parser does not actively extract a name. |
| `email` | string or null | Encrypted candidate email. |
| `email_idx` | string or null | Blind index for exact email search. |
| `phone` | string or null | Encrypted candidate phone. |
| `phone_idx` | string or null | Blind index for exact phone search. |
| `address` | string or null | Encrypted candidate address. |
| `address_idx` | string or null | Blind index for exact address search. |
| `skills` | string or null | Comma-separated extracted skills. |
| `soft_skills` | string or null | Comma-separated extracted soft skills. |
| `story` | string or null | Generated career story. |
| `experience` | string or null | Comma-separated extracted experience entries. |
| `education` | string or null | Comma-separated extracted education entries. |
| `resume` | string | Uploaded resume file URL/path. |
| `created_at` | datetime or null | Record creation timestamp. |
| `updated_at` | datetime or null | Last update timestamp. |

### Skill

| Field | Type | Notes |
| --- | --- | --- |
| `id` | integer | Skill primary key. |
| `name` | string | Skill name. |

### Education

| Field | Type | Notes |
| --- | --- | --- |
| `id` | integer | Education primary key. |
| `name` | string | Education name. |
| `short_form` | string or null | Optional short form, not set by the bulk-create endpoint. |

## Environment Variables

The current backend expects these values in `.env`:

```text
OPENAI_API_KEY=<OpenAI API key>
PII_ENCRYPTION_KEY=<Fernet key>
BLIND_INDEX_KEY=<secret string for HMAC indexes>
```

Security notes:

| Variable | Purpose |
| --- | --- |
| `OPENAI_API_KEY` | Used to call OpenAI for generated career stories. |
| `PII_ENCRYPTION_KEY` | Used by Fernet to encrypt/decrypt candidate personal information. |
| `BLIND_INDEX_KEY` | Used to generate deterministic HMAC indexes for exact search on encrypted PII. |

Do not commit `.env` or real keys to version control.

## Implementation Notes and Current Limitations

| Area | Current behavior |
| --- | --- |
| PDF validation | Validation checks only that the uploaded filename ends with `.pdf`. |
| CV upload failures | Malformed PDFs or OpenAI errors are not currently wrapped in custom error responses. |
| OpenAI response parsing | The response is expected to be valid JSON containing a `story` key. |
| Dynamic-data permissions | Bulk skill and education creation endpoints are public in the current implementation. |
| Token refresh endpoint | No refresh endpoint is currently registered in `urls.py`, even though Simple JWT is installed. |
| PII response exposure | `/cv/story-data/` currently serializes encrypted personal fields and blind indexes. |
| Search by address | `address_idx` is stored, but there is no public endpoint that searches by address. |
