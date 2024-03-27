// components/AuthWrapper.tsx
import { useRouter } from 'next/router';
import { useDispatch, useSelector } from 'react-redux';
import { getValidAuthTokens } from '@/lib/cookies';
import { useGetAuthDataQuery } from '@/lib/api/authApi';
import { useEffect } from 'react';
import { useAppDispatch, RootState } from '@/lib/store';

type Props = {
  children?: React.ReactNode;
};

export const AuthWrapper = ({ children }: Props) => {
  const dispatch = useAppDispatch();
  const { push } = useRouter();
  // const { username:any } = useSelector((state: RootState) => state.auth);

  const { token } = getValidAuthTokens();

  // this query will only execute if the token is valid and the user email is not already in the redux store
  const { error, isLoading } = useGetAuthDataQuery(
    { token: token || '' },
    // {
    //   // The useGetAuthDataQuery hook will not execute the query at all if these values are falsy
    //   skip: !!username || !token,
    // }
  );

  // if the user doesnt have a valid token, redirect to login page
  useEffect(() => {
    if (!token) {
      push('/login');
      // will explain this in a moment
      dispatch(logout());
    }
  }, [token, push]);

  // optional: show a loading indicator while the query is loading
  if (isLoading) {
    return <div>Loading...</div>;
  }

  return children;
};