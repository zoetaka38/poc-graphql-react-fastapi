import { graphql } from "src/gql";

export const FETCH_USERS = graphql(`
  query FetchUsers {
    users {
      id
      name
      stickynotes {
        id
        text
      }
    }
  }
`);

export const FETCH_NOTES = graphql(`
  query FetchNotes {
    stickynotes {
      id
      text
    }
  }
`);
