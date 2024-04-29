import React from 'react';

const DemoImages = ({ onDemoImageClick }) => {
  return (
    <section className="demo-images">
      <h2>Demo Images</h2>
      <img src="demo-image1.jpg" alt="" className="demo-image" onClick={() => onDemoImageClick('demo-1')} />
      <img src="demo-image2.jpg" alt="" className="demo-image" onClick={() => onDemoImageClick('demo-2')} />
      <img src="demo-image3.jpg" alt="" className="demo-image" onClick={() => onDemoImageClick('demo-3')} />
    </section>
  );
};

export default DemoImages;
