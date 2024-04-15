/* eslint-disable jsx-a11y/alt-text */
"use client";

import Image from "next/image";
import { useEffect, useState } from "react";

const ImageFallback = (props: any) => {
  const { src, fallback, ...rest } = props;
  const [imgSrc, setImgSrc] = useState(src);

  useEffect(() => {
    setImgSrc(src);
  }, [src]);

  return (
    <Image
      {...rest}
      src={imgSrc ?? `/images/image-placeholder.png`}
      onError={() => {
        setImgSrc(fallback ?? '/images/image-placeholder.png');
      }}
    />
  );
};

export default ImageFallback;
