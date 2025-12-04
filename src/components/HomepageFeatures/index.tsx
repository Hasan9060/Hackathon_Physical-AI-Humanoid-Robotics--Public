import React from 'react';
import clsx from 'clsx';
import styles from './styles.module.css';

type FeatureItem = {
  title: string;
  Svg: React.ComponentType<React.SVGProps<SVGSVGElement>>;
  description: JSX.Element;
};

const FeatureList: FeatureItem[] = [
  {
    title: '13-Week Curriculum',
    Svg: require('@site/static/img/undraw_docusaurus_tree.svg').default,
    description: (
      <>
        Comprehensive 13-week curriculum covering ROS 2, simulation, AI control,
        and VLA integration for humanoid robotics education.
      </>
    ),
  },
  {
    title: 'Hardware Specifications',
    Svg: require('@site/static/img/undraw_docusaurus_mountain.svg').default,
    description: (
      <>
        Detailed procurement guides for Digital Twin Workstations, Edge AI Kits,
        and Robot Lab configurations with cost analysis.
      </>
    ),
  },
  {
    title: 'Technical Architecture',
    Svg: require('@site/static/img/undraw_docusaurus_react.svg').default,
    description: (
      <>
        Complete system architecture documentation with Sim-to-Real transfer
        workflows and integration patterns.
      </>
    ),
  },
];

function Feature({title, Svg, description}: FeatureItem) {
  return (
    <div className={clsx('col col--4', styles.feature)}>
      <div className="text--center">
        <Svg className={styles.featureSvg} role="img" />
      </div>
      <div className="text--center padding-horiz--md">
        <h3>{title}</h3>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures(): JSX.Element {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}