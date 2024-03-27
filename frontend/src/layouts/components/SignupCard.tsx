"use client";

import { useSignupMutation } from "@/lib/api/authApi";
import { SignupResponse } from "@/types";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { Button, TextField } from "@mui/material";
import { toast } from "react-toastify";

const SignupCard = () => {
  const [signupState, setState] = useState({
    first_name: "",
    last_name: "",
    username: "",
    password: "",
    confirm_password: "",
  });
  const router = useRouter();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    console.log("handleChange", e.target.name, e.target.value)
    setState({...signupState, [e.target.name]: e.target.value });
  };
  const [signup, { isLoading, isError, error }] = useSignupMutation();

  const handleSubmit = async (e: any) => {
    e.preventDefault();

    try {
      if (!signupState.username || !signupState.password) {
        throw new Error("Invalid username or password");
      }

      const response: SignupResponse = await signup(signupState).unwrap();
      
      if (response.token) {
        router.push("/");
      } else {
        throw new Error("Unable to signup");
      }
    } catch (error) {
      toast.error("Unable to signup. Please try again.");
      // setState({ ...signupState, password: "", confirm_password: "" });
    }
  }
  return (
      <>
        <section>
          <div className="flex flex-col items-center justify-center  md:h-6.5 py-3">
              <div className="w-full bg-white rounded-lg shadow dark:border md:mt-0 sm:max-w-md xl:p-0 dark:bg-gray-600 dark:border-gray-700">
                  <div className="p-6 space-y-4 md:space-y-6 sm:p-8">
                      <h1 className="text-xl font-bold leading-tight tracking-tight text-gray-900 md:text-2xl dark:text-white">
                          Sign up
                      </h1>
                      <form className="space-y-4 md:space-y-6" onSubmit={handleSubmit}>
                          <div>
                              <label className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">First Name</label>
                              <input onChange={handleChange} value={signupState.first_name} type="text" name="first_name" id="first_name" className="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="First Name" required/>
                          </div>
                          <div>
                              <label className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Last Name</label>
                              <input onChange={handleChange} value={signupState.last_name} type="text" name="last_name" id="last_name" className="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="Last Name" required/>
                          </div>
                          <div>
                              <label className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">username</label>
                              <input onChange={handleChange} value={signupState.username} type="text" name="username" id="username" className="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="username" required/>
                          </div>
                          <div>
                              <label className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Password</label>
                              <input onChange={handleChange} value={signupState.password} type="password" name="password" id="password" placeholder="••••••••" className="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" required/>
                          </div>
                          <div>
                              <label className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Confirm Password</label>
                              <input onChange={handleChange} value={signupState.confirm_password} type="password" name="confirm_password" id="confirm_password" placeholder="••••••••" className="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" required />
                          </div>
                          {/* <div className="flex items-center justify-between">
                              <div className="flex items-start">
                                  <div className="flex items-center h-5">
                                    <input id="remember" aria-describedby="remember" type="checkbox" className="w-4 h-4 border border-gray-300 rounded bg-gray-50 focus:ring-3 focus:ring-primary-300 dark:bg-gray-700 dark:border-gray-600 dark:focus:ring-primary-600 dark:ring-offset-gray-800" required=""/>
                                  </div>
                                  <div className="ml-3 text-sm">
                                    <label className="text-gray-500 dark:text-gray-300">Remember me</label>
                                  </div>
                              </div>
                              <a href="#" className="text-sm font-medium text-primary-600 hover:underline dark:text-primary-500">Forgot password?</a>
                          </div> */}

                          <Button className="w-full dark:text-white bg-primary-600 dark:hover:bg-primary-700 focus:ring-4 focus:outline-none focus:ring-primary-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-primary-600 dark:hover:bg-primary-700 dark:focus:ring-primary-800" onClick={handleSubmit}>
                            { isLoading ? "Loading..." : "Signup" }
                          </Button>
                          {/* <p className="text-sm font-light text-gray-500 dark:text-gray-400">
                              Don’t have an account yet? <a href="#" className="font-medium text-primary-600 hover:underline dark:text-primary-500">Sign up</a>
                          </p> */}
                      </form>
                  </div>
              </div>
          </div>
        </section>
      </>
  )
};

export default SignupCard;