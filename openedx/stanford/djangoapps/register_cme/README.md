# Instructions

- Add `openedx.stanford.djangoapps.register_cme` to the
  `ADDL_INSTALLED_APPS` array in `lms.env.json`.
- Set `REGISTRATION_EXTENSION_FORM` to
  `openedx.stanford.djangoapps.register_cme.forms.ExtraInfoForm` in
  `lms.env.json`.
- Run migrations.
- (optionally) Migrate legacy data with the `migrate_legacy_cme_data`
  management command.
- Start/restart the LMS.
