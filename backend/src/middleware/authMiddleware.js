module.exports = (req, res, next) => {
  // Add authentication logic here
  console.log('Middleware executed');
  next();
};

