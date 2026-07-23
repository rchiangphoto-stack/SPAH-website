/* SPAH conversion tracking — GA4 custom events
 *
 * Why this exists: GA4 was installed sitewide but only recorded pageviews, so
 * there was no way to tell which pages actually produced appointments. The
 * booking link leaves for an external ezyVet domain, which is exactly where
 * GA4 lost the user.
 *
 * Events sent:
 *   book_appointment_click  — any link to the ezyVet booking portal
 *   phone_call_click        — any tel: link
 *   email_click             — any mailto: link
 *   contact_form_submit     — submission of any on-page form
 *   pharmacy_click          — outbound to the Koala pharmacy
 *
 * Each carries: page_path, link_text, link_url, and page_section (nav / hero /
 * footer / sticky-cta / body) so we can see WHERE on the page people convert.
 *
 * NOTE: sending the event is only half the job — each of these must also be
 * marked as a "key event" (conversion) in the GA4 admin UI before it shows up
 * in conversion reports.
 */
(function () {
  'use strict';

  function send(name, params) {
    if (typeof window.gtag !== 'function') return;
    try {
      window.gtag('event', name, params);
    } catch (e) { /* never let tracking break the page */ }
  }

  // Which part of the page was the click in? Helps compare hero vs footer vs sticky bar.
  function sectionOf(el) {
    var n = el;
    while (n && n !== document.body) {
      if (n.id === 'sticky-cta') return 'sticky_cta';
      var tag = (n.tagName || '').toLowerCase();
      if (tag === 'nav') return 'nav';
      if (tag === 'footer') return 'footer';
      if (tag === 'header') return 'header';
      if (tag === 'section') {
        var h = n.querySelector('h1, h2');
        if (h) {
          var t = (h.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 40);
          if (t) return t;
        }
        return 'section';
      }
      n = n.parentNode;
    }
    return 'body';
  }

  function base(a) {
    return {
      page_path: location.pathname,
      page_title: document.title.slice(0, 90),
      link_text: (a.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 60),
      link_url: a.getAttribute('href') || '',
      page_section: sectionOf(a)
    };
  }

  // Delegated so it covers links added after load (sticky CTA, mobile menu, etc.)
  document.addEventListener('click', function (ev) {
    var a = ev.target && ev.target.closest ? ev.target.closest('a[href]') : null;
    if (!a) return;
    var href = a.getAttribute('href') || '';

    if (href.indexOf('ezyvet.com') > -1) {
      send('book_appointment_click', base(a));
    } else if (href.indexOf('tel:') === 0) {
      send('phone_call_click', base(a));
    } else if (href.indexOf('mailto:') === 0) {
      send('email_click', base(a));
    } else if (href.indexOf('koala.health') > -1) {
      send('pharmacy_click', base(a));
    }
  }, true); // capture phase: fires even if something later stops propagation

  document.addEventListener('submit', function (ev) {
    var f = ev.target;
    if (!f || f.tagName !== 'FORM') return;
    send('contact_form_submit', {
      page_path: location.pathname,
      page_title: document.title.slice(0, 90),
      form_id: f.id || f.getAttribute('name') || 'unnamed',
      page_section: sectionOf(f)
    });
  }, true);
})();
