import { useQuery, useSubscription } from "@apollo/client";
import { useEffect, useState } from "react";
import { FETCH_USERS } from "src/apollo/GraphQL/Queries";
import { SUBSCRIBE_NOTES } from "src/apollo/Subscription";
import { StickyNoteScalar, UserScalar } from "src/gql/graphql";

const UserList = () => {
  const [users, setUsers] = useState<UserScalar[]>([]);
  const onNoteSubscribe = (newNote: StickyNoteScalar) => {
    console.log("newNote", newNote);
    if (newNote === null) return;
    setUsers((prev) => {
      const updatedUsers = prev.map((user) => {
        if (user.id === newNote.userId) {
          return {
            ...user,
            stickynotes: [...user.stickynotes, newNote],
          };
        }
        return user;
      });
      return updatedUsers;
    });
  };

  const { loading, error, data } = useQuery(FETCH_USERS);
  const { data: subscriptionData } = useSubscription(SUBSCRIBE_NOTES, {
    onData: ({ data }) => {
      if (data && data.data && data.data.subscribeStickynote) {
        onNoteSubscribe(data.data.subscribeStickynote);
      }
    },
  });

  useEffect(() => {
    if (data && data.users) {
      setUsers(
        data.users.map((user: any) => ({
          ...user,
          stickynotes: user.stickynotes || [],
        }))
      );
    }
  }, [data]);

  if (loading) return <p>...loading</p>;
  if (error) return <p>{error.message}</p>;

  return (
    <div>
      <h2>User List</h2>
      {users.map((user: UserScalar) => (
        <div key={user.id} style={{ textAlign: "left" }}>
          <div>
            ・{user.id}: {user.name}
          </div>
          {user.stickynotes.map((note: any) => (
            <div key={note.id} style={{ marginLeft: "16px" }}>
              ・{note.id}: {note.text}
            </div>
          ))}
        </div>
      ))}
    </div>
  );
};

export default UserList;
