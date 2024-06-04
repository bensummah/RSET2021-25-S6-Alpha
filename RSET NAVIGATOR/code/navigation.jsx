import React from 'react';
import { useLocation } from 'react-router-dom';


function NavigationPage() {
 

  return (
    <div className='navigation-container'>
     
      <iframe
        id="map-viewer-iframe"
        style={{ width: '100%', height: '600px' }}
        src="https://map-viewer.situm.com?apikey=7d62938fb9a6b92b3d38507c010e5fdeaca0c45502b8783abfe1884a8e86fb58&domain="
      ></iframe>
    </div>
  );
}

export default NavigationPage;