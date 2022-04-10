import React from 'react';
import { Route, Redirect } from "react-router-dom";

function SimpleRoute({ exact, component: Component, path, ...props }) {
  return (
    <Route path={path} exact={exact}>
      {
        () => <Component {...props} />
      }
    </Route>
  )
}
export default SimpleRoute;