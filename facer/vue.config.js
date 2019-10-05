module.exports = {
    devServer: {
        disableHostCheck: true,
        host : '0.0.0.0',
        // proxy: {
        //     '/api': {
        //         target: 'http://127.0.0.1:8000/api',
        //         changeOrigin: true,
        //         pathRewrite: {
        //             '^/api': ''
        //         }
        //     }
        // }
    }
}


