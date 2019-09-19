module.exports = {
    devServer: {
        proxy: {
            '/api': {
                target: 'http://localhost:8000/api',
                changeOrigin: true,
                pathRewrite: {
                    '^/api': ''
                }
            }
        }
    }
}


