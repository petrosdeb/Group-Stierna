# MainActivity
**MainActivity** is the main class that runs on the UI-thread, or main thread, for **Group Stierna**'s app that is used to control a **MOPED**.
It uses **RadioButton**s, **SeekBar**s, and **EditText**s to allow the user to control the **MOPED**.
To connect and send commands to the **MOPED** the **MainActivity** uses a **StiernaAsyncClient** (see more below) which is called every time a **RadioButton** is checked, whenever the Connect **Button** is pressed, or an enabled **SeekBar**'s value is changed, with teh exception of ACC-speed during Manual driving mode.
A **Handler** is used to determine whether or not the message was sent, and the current connection status is updated based on this.

To detect the changes in these UI-elements **Listener**s are used.
**TextField**s are used to display connection status and the values of the **SeekBar**s.
To further help the user the **SeekBar**s are enabled or disabled based on connection status, and chosen driving mode, see following table:

|Connection status|Active driving mode|**SeekBar**, steering|**SeekBar**, speed|**SeekBar**, ACC-speed|
|---|---|---|---|---|
|Disconnected|Any|Disabled|Disabled|Disabled|
|Connected|Manual|Enabled|Enabled|Enabled|
|Connected|ACC|Enabled|Disabled|Enabled|
|Connected|Platooning|Disabled|Disabled|Enabled|

# StiernaAsyncClient
**StiernaAsyncClient** is a subclass of **AsyncTask** which is used for threading in Android.
**StiernaAsyncClient** accepts an IP-address in the form of a **String**, a port number in the form of an **int**, a message in the form of a **String**, and a **Handler** for sending back information to the UI-thread.
When **StiernaAsyncClient** is instansiated it tries to create a socket going to the IP and port entered.
If the connection was successful the message is sent via the socket before the socket is closed.
Finally the **Handler** is given a **Boolean** which is true if the connection was successful, and false otherwise.
