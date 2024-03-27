"use client"

import { useTheme } from "next-themes";
import { ToastContainer } from "react-toastify";
import 'react-toastify/dist/ReactToastify.css';

const CustomToastContainer = () => {
  const { theme } = useTheme();
  return (
    <ToastContainer
      position="top-right"
      autoClose={5000}
      hideProgressBar={false}
      newestOnTop={true}
      closeOnClick
      rtl={false}
      pauseOnFocusLoss={false}
      draggable
      pauseOnHover={false}
      theme = {theme === "dark" ? "dark" : "light"}
    />
  );
}

export default CustomToastContainer;
