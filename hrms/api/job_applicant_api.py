import frappe
import json

@frappe.whitelist()
def send_bulk_applicant_email_bcc_split(applicants, subject=None, message=None, template=None):

    if isinstance(applicants, str):
        applicants = json.loads(applicants)

    email_list = []

    for name in applicants:
        doc = frappe.get_doc("Job Applicant", name)
        if doc.email_id:
            email_list.append(doc.email_id)

    if not email_list:
        frappe.throw("No valid emails found")

    # 🔥 Split logic
    to_email = email_list[0]          # first applicant
    bcc_list = email_list[1:]         # rest

    # 🔥 Template (optional)
    if template:
        temp = frappe.get_doc("Email Template", template)
        subject = temp.subject
        message = temp.response

    frappe.sendmail(
        recipients=[to_email],        # 👈 first one
        bcc=bcc_list,                # 👈 rest
        sender="crm.noreply@b2bexportsllc.com",
	subject=subject,
        message=message,
        now=False
    )

    return f"Email sent: 1 TO + {len(bcc_list)} BCC"
