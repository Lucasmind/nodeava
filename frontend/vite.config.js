import { defineConfig } from 'vite';
import { join } from 'path';
import { existsSync, readFileSync } from 'fs';

// Serves ONNX Runtime WASM/worker files directly, bypassing Vite's module
// transform pipeline which chokes on the ?import suffix for these files.
// Required by VAD-web (Silero via onnxruntime-web).
function serveOnnxFiles() {
  const publicVadDir = join(process.cwd(), 'public/vad');
  return {
    name: 'serve-onnx-files',
    configureServer(server) {
      server.middlewares.use((req, res, next) => {
        const url = req.url?.split('?')[0];
        if (!url?.startsWith('/vad/ort-wasm-simd-threaded')) return next();

        const filename = url.split('/').pop();
        const filepath = join(publicVadDir, filename);

        if (existsSync(filepath)) {
          const ext = filename.split('.').pop();
          const types = { mjs: 'application/javascript', wasm: 'application/wasm' };
          res.setHeader('Content-Type', types[ext] || 'application/octet-stream');
          res.setHeader('Access-Control-Allow-Origin', '*');
          res.end(readFileSync(filepath));
          return;
        }
        next();
      });
    },
  };
}

export default defineConfig({
  root: '.',
  publicDir: 'public',
  build: {
    outDir: 'dist',
    assetsInlineLimit: 0,
  },
  plugins: [serveOnnxFiles()],
  server: {
    port: 3000,
    host: true,
    proxy: {
      '/api/stt': {
        target: 'http://localhost:8080',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api\/stt/, ''),
      },
      '/api/llm': {
        target: 'http://localhost:8081',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api\/llm/, ''),
      },
      '/api/tts': {
        target: 'http://localhost:8880',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api\/tts/, ''),
      },
    },
  },
  assetsInclude: ['**/*.glb'],
  optimizeDeps: {
    exclude: ['@met4citizen/talkinghead'],
  },
});
