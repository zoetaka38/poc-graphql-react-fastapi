import { graphql } from "src/gql";

export const SUBSCRIBE_NOTES = graphql(`
  subscription SubscribeNotes {
    subscribeStickynote {
      createdDatetime
      id
      text
      userId
    }
  }
`);
