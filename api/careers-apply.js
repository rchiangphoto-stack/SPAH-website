// api/careers-apply.js
// Requires: npm install resend
// Env var needed: RESEND_API_KEY

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const RESEND_API_KEY = process.env.RESEND_API_KEY;
  if (!RESEND_API_KEY) {
    return res.status(500).json({ error: 'Email service not configured' });
  }

  try {
    const {
      name, email, phone, linkedin, position, hearAbout,
      message, resumeBase64, resumeName, resumeType
    } = req.body;

    // Validate required fields
    if (!name || !email || !message) {
      return res.status(400).json({ error: 'Missing required fields' });
    }

    const attachments = [];
    if (resumeBase64 && resumeName) {
      attachments.push({
        filename: resumeName,
        content: resumeBase64,
        encoding: 'base64'
      });
    }

    // 1. Send application email to careers@spah.la
    const notifyRes = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${RESEND_API_KEY}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        from: 'SPAH Careers <onboarding@resend.dev>',
        to: ['careers@spah.la'],
        subject: `New Application: ${position} — ${name}`,
        html: `
          <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 24px; background: #FAFAF8;">
            <div style="background: #5A7FA6; color: white; padding: 20px 24px; border-radius: 12px 12px 0 0;">
              <h2 style="margin:0; font-size: 1.3rem;">New Job Application — SPAH</h2>
              <p style="margin: 4px 0 0; opacity: 0.8; font-size: 0.9rem;">${position}</p>
            </div>
            <div style="background: white; padding: 24px; border-radius: 0 0 12px 12px; border: 1px solid #e0e8f0;">
              <table style="width: 100%; border-collapse: collapse;">
                <tr><td style="padding: 8px 0; color: #5C6B7A; width: 140px; font-size: 0.9rem;">Name</td><td style="padding: 8px 0; font-weight: bold; color: #2A3442;">${name}</td></tr>
                <tr><td style="padding: 8px 0; color: #5C6B7A; font-size: 0.9rem;">Email</td><td style="padding: 8px 0; color: #2A3442;"><a href="mailto:${email}">${email}</a></td></tr>
                <tr><td style="padding: 8px 0; color: #5C6B7A; font-size: 0.9rem;">Phone</td><td style="padding: 8px 0; color: #2A3442;">${phone || '—'}</td></tr>
                <tr><td style="padding: 8px 0; color: #5C6B7A; font-size: 0.9rem;">LinkedIn</td><td style="padding: 8px 0; color: #2A3442;">${linkedin ? `<a href="${linkedin}">${linkedin}</a>` : '—'}</td></tr>
                <tr><td style="padding: 8px 0; color: #5C6B7A; font-size: 0.9rem;">Position</td><td style="padding: 8px 0; color: #2A3442;"><strong>${position}</strong></td></tr>
                <tr><td style="padding: 8px 0; color: #5C6B7A; font-size: 0.9rem;">Heard via</td><td style="padding: 8px 0; color: #2A3442;">${hearAbout || '—'}</td></tr>
              </table>
              <div style="margin-top: 16px; padding: 16px; background: #EFF4F9; border-radius: 8px;">
                <p style="margin: 0 0 8px; color: #5C6B7A; font-size: 0.85rem; font-weight: bold; text-transform: uppercase; letter-spacing: 0.05em;">Cover Letter / Message</p>
                <p style="margin: 0; color: #2A3442; white-space: pre-wrap; line-height: 1.6;">${message}</p>
              </div>
              ${resumeName ? `<p style="margin-top: 16px; color: #5C6B7A; font-size: 0.9rem;">📎 Resume attached: <strong>${resumeName}</strong></p>` : '<p style="margin-top: 16px; color: #5C6B7A; font-size: 0.9rem;">No resume attached.</p>'}
            </div>
          </div>
        `,
        attachments
      })
    });

    if (!notifyRes.ok) {
      const errBody = await notifyRes.text();
      console.error('Resend notify error:', errBody);
      return res.status(500).json({ error: 'Failed to send notification email' });
    }

    // 2. Send confirmation to applicant
    await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${RESEND_API_KEY}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        from: 'SPAH Careers <onboarding@resend.dev>',
        to: [email],
        subject: 'We received your application — South Pasadena Animal Hospital',
        html: `
          <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 24px; background: #FAFAF8;">
            <div style="background: linear-gradient(135deg, #5A7FA6, #7A9E8E); color: white; padding: 28px 24px; border-radius: 12px 12px 0 0; text-align: center;">
              <h2 style="margin: 0; font-size: 1.4rem;">Thank you, ${name}!</h2>
            </div>
            <div style="background: white; padding: 28px 24px; border-radius: 0 0 12px 12px; border: 1px solid #e0e8f0;">
              <p style="color: #2A3442; line-height: 1.7; margin: 0 0 16px;">We've received your application for <strong>${position}</strong> at South Pasadena Animal Hospital.</p>
              <p style="color: #2A3442; line-height: 1.7; margin: 0 0 16px;">Our team reviews every application personally. If your background is a fit for our team, we'll be in touch within two weeks to schedule a conversation.</p>
              <p style="color: #5C6B7A; line-height: 1.7; margin: 0 0 24px; font-size: 0.95rem;">Thank you for your interest in joining SPAH — we appreciate your time.</p>
              <div style="border-top: 1px solid #e0e8f0; padding-top: 20px; margin-top: 8px;">
                <p style="margin: 0; color: #5C6B7A; font-size: 0.85rem;">South Pasadena Animal Hospital<br>3116 W Main St, Alhambra, CA 91801<br><a href="mailto:careers@spah.la" style="color: #5A7FA6;">careers@spah.la</a></p>
              </div>
            </div>
          </div>
        `
      })
    });

    return res.status(200).json({ success: true });

  } catch (err) {
    console.error('careers-apply error:', err);
    return res.status(500).json({ error: 'Internal server error' });
  }
}
