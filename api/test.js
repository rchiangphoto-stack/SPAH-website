module.exports = function handler(req, res) {
  res.status(200).json({ ok: true, body: req.body, method: req.method });
};
