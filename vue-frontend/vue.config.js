module.exports = {
    devServer: {
      proxy: {
        '^/api': {
          target: 'http://58.87.86.11:7001',
          changeOrigin: true
        },
      }
    }
  }