import { fileURLToPath, URL } from "node:url"
import { createVuePlugin } from "vite-plugin-vue2"
import { VuetifyResolver } from "unplugin-vue-components/resolvers"
import Components from "unplugin-vue-components/vite"
import eslintPlugin from "vite-plugin-eslint"

export default {
    plugins: [
        createVuePlugin(),
        Components({
            resolvers: [VuetifyResolver()]
        }),
        eslintPlugin({
            include: [
                "src/**/*.js",
                'src/**/*.vue', 
                'src/*.js', 
                'src/*.vue'
            ]
        })
    ],
    resolve: {
        alias: { '~': fileURLToPath(new URL('src', import.meta.url)) }
    },
    build: {
    }
}