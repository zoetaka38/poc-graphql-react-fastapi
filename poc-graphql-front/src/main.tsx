import {
  ApolloClient,
  ApolloProvider,
  createHttpLink,
  InMemoryCache,
} from "@apollo/client";
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import App from "./App";
import "./index.css";

const link = createHttpLink({
  uri: "http://localhost:8010/graphql",
  credentials: "include",
});

const client = new ApolloClient({
  cache: new InMemoryCache({ addTypename: false }),
  link: link,
});

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <ApolloProvider client={client}>
      <App />
    </ApolloProvider>
  </StrictMode>
);
