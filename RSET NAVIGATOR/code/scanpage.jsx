// src/ScanPage.js

import React, { useState, useEffect, useRef } from 'react';
import jsQR from 'jsqr';
import { useNavigate } from 'react-router-dom';

function ScanPage() {
  const [qrData, setQrData] = useState(null);
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const navigate = useNavigate();

  useEffect(() => {
    const video = videoRef.current;
    navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } }).then(stream => {
      video.srcObject = stream;
      video.play();

      const tick = () => {
        const canvas = canvasRef.current;
        if (video.readyState === video.HAVE_ENOUGH_DATA && canvas) {
          const context = canvas.getContext('2d');
          canvas.height = video.videoHeight;
          canvas.width = video.videoWidth;
          context.drawImage(video, 0, 0, canvas.width, canvas.height);
          const imageData = context.getImageData(0, 0, canvas.width, canvas.height);
          const code = jsQR(imageData.data, imageData.width, imageData.height, {
            inversionAttempts: 'dontInvert',
          });
          if (code) {
            setQrData(code.data);
            stream.getTracks().forEach(track => track.stop());
          }
        }
        requestAnimationFrame(tick);
      };
      requestAnimationFrame(tick);
    }).catch(error => {
      console.error('Error accessing camera', error);
    });
  }, []);

  useEffect(() => {
    if (qrData) {
      navigate(`/navigate?${qrData}`);
    }
  }, [qrData, navigate]);

  return (
    <div className='scan-container'>
      <h2>Scanning...</h2>
      <div className='video-container'>
        <video ref={videoRef} className='video' />
        <canvas ref={canvasRef} className='hidden-canvas' />
      </div>
    </div>
  );
}

export default ScanPage;