module.exports = {
    devServer: {
      proxy: {
        '^/api': {
          target: 'http://58.87.86.11:8000',
          changeOrigin: true
        },
      }
    }
  }