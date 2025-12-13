import type { Config } from '@docusaurus/types';
import type { Options as ThemeConfig } from '@docusaurus/preset-classic';

const config: Config = {
  title: 'Physical AI & Humanoid Robotics Lab',
  tagline: 'A Complete Guide to Building Academic Robotics Infrastructure',
  favicon: 'img/favicon.ico',

  // Set the production url of your site here
  url: 'https://humanoid-robotics-textbook.netlify.app',
  // Set the /<baseUrl>/ pathname under which your site is served
  baseUrl: '/',

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: 'hasanrafay',
  projectName: 'humanoid-robotics-textbook',

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  // Even if you don't use internationalization, you can still use
  // this field to set useful metadata like html lang. For example, if
  // your site is Chinese, you may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'ur'],
    localeConfigs: {
      ur: {
        label: 'اردو',
        direction: 'rtl',
        htmlLang: 'ur-PK',
        calendar: 'gregory',
      },
    },
  },

  // Custom fields for API configuration
  customFields: {
    apiUrl: process.env.API_URL || 'http://localhost:8000',
  },


  presets: [
    [
      'classic',
      {
        docs: false,
        blog: false,
        theme: {
          customCss: ['./src/css/custom.css'],
        },
      } satisfies Options,
    ],
  ],

  themeConfig: {
    navbar: {
      title: 'Physical AI & Humanoid Robotics Lab',
      logo: {
        alt: 'Robotics Lab Logo',
        src: 'img/logo.svg',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'tutorialSidebar',
          position: 'left',
          label: 'Curriculum',
          docsPluginId: 'tutorial',
        },
        {
          href: 'https://github.com/hasanrafay/humanoid-robotics-textbook',
          label: 'GitHub',
          position: 'right',
        },
        {
          type: 'custom-auth',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Resources',
          items: [
            {
              label: 'ROS 2 Documentation',
              href: 'https://docs.ros.org/en/rolling/',
            },
            {
              label: 'NVIDIA Isaac Sim',
              href: 'https://developer.nvidia.com/isaac-sim',
            },
          ],
        },
        {
          title: 'Community',
          items: [
            {
              label: 'Stack Overflow',
              href: 'https://stackoverflow.com/questions/tagged/docusaurus',
            },
            {
              label: 'Discord',
              href: 'https://discordapp.com/invite/docusaurus',
            },
            {
              label: 'Twitter',
              href: 'https://twitter.com/docusaurus',
            },
          ],
        },
        {
          title: 'More',
          items: [
            {
              label: 'Blog',
              to: '/blog',
            },
            {
              label: 'GitHub',
              href: 'https://github.com/hasanrafay/humanoid-robotics-textbook',
            },
          ],
        },
      ],
      copyright: `Copyright © 2025 Hasan Rafay. Built with Docusaurus.`,
    },
    colorMode: {
      defaultMode: 'dark',
      disableSwitch: false,
      respectPrefersColorScheme: true,
    },
    docs: {
      sidebar: {
        hideable: true,
      },
    },
    prism: {
      theme: require('prism-react-renderer').themes.github,
      darkTheme: require('prism-react-renderer').themes.dracula,
    },
  } satisfies ThemeConfig,

  plugins: [
    [
      '@docusaurus/plugin-content-docs',
      {
        id: 'tutorial',
        path: 'docs',
        routeBasePath: '/',
        sidebarPath: './sidebars.ts',
        // ... other options
      },
    ],
  ],
};

export default config;