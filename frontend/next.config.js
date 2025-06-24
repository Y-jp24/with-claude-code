/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  output: 'standalone',
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1'
  },
  async rewrites() {
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1'
    const baseUrl = apiUrl.replace('/api/v1', '')
    return [
      {
        source: '/api/:path*',
        destination: `${baseUrl}/api/:path*`
      }
    ]
  }
}

module.exports = nextConfig