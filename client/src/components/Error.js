import { useRouteError } from "react-router-dom";

const Error = () => {
  const error = useRouteError();
  return <div>{error?.error?.message}</div>;
};

export default Error;