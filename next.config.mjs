/** @type {import('next').NextConfig} */
const nextConfig = {
  // Performance Optimizations
  compress: true,                     // Enable gzip compression
  productionBrowserSourceMaps: false, // Disable source maps in production
  
  // Image Optimization
  images: {
    unoptimized: false,
    formats: ['image/avif', 'image/webp'], // Modern image formats
    deviceSizes: [640, 750, 828, 1080, 1200, 1920, 2048, 3840],
    imageSizes: [16, 32, 48, 64, 96, 128, 256, 384],
  },

  // Headers for security and caching
  async headers() {
    return [
      {
        source: '/:path*',
        headers: [
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff',
          },
          {
            key: 'X-Frame-Options',
            value: 'DENY',
          },
          {
            key: 'X-XSS-Protection',
            value: '1; mode=block',
          },
          {
            key: 'Referrer-Policy',
            value: 'strict-origin-when-cross-origin',
          },
        ],
      },
      // Cache static assets for 1 year
      {
        source: '/assets/:path*',
        headers: [
          {
            key: 'Cache-Control',
            value: 'public, max-age=31536000, immutable',
          },
        ],
      },
    ];
  },

  // Redirects (optional)
  async redirects() {
    return [];
  },

  // Rewrites (already in vercel.json, but can also be here)
  async rewrites() {
    return {
      beforeFiles: [],
      afterFiles: [
        {
          source: '/:path*',
          destination: '/:path*',
        },
      ],
    };
  },
};

export default nextConfig;
