/* eslint-disable */
import { TypedDocumentNode as DocumentNode } from '@graphql-typed-document-node/core';
export type Maybe<T> = T | null;
export type InputMaybe<T> = Maybe<T>;
export type Exact<T extends { [key: string]: unknown }> = { [K in keyof T]: T[K] };
export type MakeOptional<T, K extends keyof T> = Omit<T, K> & { [SubKey in K]?: Maybe<T[SubKey]> };
export type MakeMaybe<T, K extends keyof T> = Omit<T, K> & { [SubKey in K]: Maybe<T[SubKey]> };
export type MakeEmpty<T extends { [key: string]: unknown }, K extends keyof T> = { [_ in K]?: never };
export type Incremental<T> = T | { [P in keyof T]?: P extends ' $fragmentName' | '__typename' ? T[P] : never };
/** All built-in and custom scalars, mapped to their actual values */
export type Scalars = {
  ID: { input: string; output: string; }
  String: { input: string; output: string; }
  Boolean: { input: boolean; output: boolean; }
  Int: { input: number; output: number; }
  Float: { input: number; output: number; }
  /** Date with time (isoformat) */
  DateTime: { input: any; output: any; }
};

export type AddStickyNotesResponse = StickyNoteScalar | UserNameMissing | UserNotFound;

export type AddUser = {
  __typename?: 'AddUser';
  id: Scalars['Int']['output'];
  name?: Maybe<Scalars['String']['output']>;
};

export type AddUserResponse = AddUser | UserExists;

export type DeleteStickyNotesResponse = StickyNoteDeleted | StickyNoteNotFound;

export type DeleteUserResponse = UserDeleted | UserIdMissing | UserNotFound;

export type Mutation = {
  __typename?: 'Mutation';
  addStickynotes: AddStickyNotesResponse;
  addUser: AddUserResponse;
  deleteStickynote: DeleteStickyNotesResponse;
  deleteUser: DeleteUserResponse;
  updateStickynote: UpdateStickyNotesResponse;
};


export type MutationAddStickynotesArgs = {
  text: Scalars['String']['input'];
  userId: Scalars['Int']['input'];
};


export type MutationAddUserArgs = {
  user: UserInput;
};


export type MutationDeleteStickynoteArgs = {
  stickynoteId: Scalars['Int']['input'];
};


export type MutationDeleteUserArgs = {
  user: UserInput;
};


export type MutationUpdateStickynoteArgs = {
  stickynoteId: Scalars['Int']['input'];
  text: Scalars['String']['input'];
};

export type Query = {
  __typename?: 'Query';
  stickynote: StickyNoteScalar;
  stickynotes: Array<StickyNoteScalar>;
  user: UserScalar;
  users: Array<UserScalar>;
};


export type QueryStickynoteArgs = {
  stickynoteId: Scalars['Int']['input'];
};


export type QueryUserArgs = {
  userId: Scalars['Int']['input'];
};

export type StickyNoteDeleted = {
  __typename?: 'StickyNoteDeleted';
  message: Scalars['String']['output'];
};

export type StickyNoteNotFound = {
  __typename?: 'StickyNoteNotFound';
  message: Scalars['String']['output'];
};

export type StickyNoteScalar = {
  __typename?: 'StickyNoteScalar';
  createdDatetime?: Maybe<Scalars['DateTime']['output']>;
  id: Scalars['Int']['output'];
  text: Scalars['String']['output'];
  userId?: Maybe<Scalars['Int']['output']>;
};

export type Subscription = {
  __typename?: 'Subscription';
  subscribeStickynote?: Maybe<StickyNoteScalar>;
};

export type UpdateStickyNotesResponse = StickyNoteNotFound | StickyNoteScalar;

export type UserDeleted = {
  __typename?: 'UserDeleted';
  message: Scalars['String']['output'];
};

export type UserExists = {
  __typename?: 'UserExists';
  message: Scalars['String']['output'];
};

export type UserIdMissing = {
  __typename?: 'UserIdMissing';
  message: Scalars['String']['output'];
};

export type UserInput = {
  id?: InputMaybe<Scalars['Int']['input']>;
  name: Scalars['String']['input'];
};

export type UserNameMissing = {
  __typename?: 'UserNameMissing';
  message: Scalars['String']['output'];
};

export type UserNotFound = {
  __typename?: 'UserNotFound';
  message: Scalars['String']['output'];
};

export type UserScalar = {
  __typename?: 'UserScalar';
  id: Scalars['Int']['output'];
  name?: Maybe<Scalars['String']['output']>;
  stickynotes: Array<StickyNoteScalar>;
};

export type FetchUsersQueryVariables = Exact<{ [key: string]: never; }>;


export type FetchUsersQuery = { __typename?: 'Query', users: Array<{ __typename?: 'UserScalar', id: number, name?: string | null, stickynotes: Array<{ __typename?: 'StickyNoteScalar', id: number, text: string }> }> };

export type FetchNotesQueryVariables = Exact<{ [key: string]: never; }>;


export type FetchNotesQuery = { __typename?: 'Query', stickynotes: Array<{ __typename?: 'StickyNoteScalar', id: number, text: string }> };

export type SubscribeNotesSubscriptionVariables = Exact<{ [key: string]: never; }>;


export type SubscribeNotesSubscription = { __typename?: 'Subscription', subscribeStickynote?: { __typename?: 'StickyNoteScalar', createdDatetime?: any | null, id: number, text: string, userId?: number | null } | null };


export const FetchUsersDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"FetchUsers"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"users"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"stickynotes"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"text"}}]}}]}}]}}]} as unknown as DocumentNode<FetchUsersQuery, FetchUsersQueryVariables>;
export const FetchNotesDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"FetchNotes"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"stickynotes"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"text"}}]}}]}}]} as unknown as DocumentNode<FetchNotesQuery, FetchNotesQueryVariables>;
export const SubscribeNotesDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"subscription","name":{"kind":"Name","value":"SubscribeNotes"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"subscribeStickynote"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"createdDatetime"}},{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"text"}},{"kind":"Field","name":{"kind":"Name","value":"userId"}}]}}]}}]} as unknown as DocumentNode<SubscribeNotesSubscription, SubscribeNotesSubscriptionVariables>;