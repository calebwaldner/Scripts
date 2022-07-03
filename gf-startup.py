#!/usr/bin/env python3.7
# Import the iterm2 python module to provide an interface for communicating with iTerm
import iterm2
import asyncio
# All the script logic goes in the main function
# `connection` holds the link to a running iTerm2 process
# `async` indicates that this function can be interrupted. This is required because
#  iTerm2 communicates with the script over a websocket connection,
#  any time the script sends/receives info from iterm2, it has to wait for a few milliseconds.

# This is where the script needs to live in order to be able to be run by iTerm2.
# /Users/calebwaldner/Library/Application Support/iTerm2/Scripts/gf-startup.py


async def main(connection):
    # Get a reference to the iterm2.App object - a singleton that provides access to iTerm2’s windows,
    # and in turn their tabs and sessions.
    app = await iterm2.async_get_app(connection)

    # Fetch the “current terminal window” from the app (returns None if there is no current window)
    window = app.current_window

    # trying to create a new window on None
    # https://iterm2.com/python-api/examples/create_window.html#create-window-example
    # if window is None:
    #     print(window)
    #     await app.async_create(connection)

    if window is not None:
        # # Add a tab to current window using the default profile
        # await window.async_create_tab()
        # # Get the active session in this tab
        # session = app.current_window.current_tab.current_session
        # # Send text to the session as though the user had typed it
        # await session.async_send_text('echo hello\n')

        # # Open another tab
        # await window.async_create_tab()
        # session = app.current_window.current_tab.current_session
        # await session.async_send_text('echo world\n')

        # Web

        webPath = '~/code/galaxy-forms-web'

        # Open VS Code for Galaxy Forms
        # await window.async_create_tab()
        session = app.current_window.current_tab.current_session
        await session.async_send_text(f'cd {webPath}\n')
        await session.async_send_text('code .\n')
        await session.async_send_text('clear\n')

        # Open VS Code for project B
        # await window.async_create_tab()
        # session = app.current_terminal_window.current_tab.current_session

        sub = await session.async_split_pane(vertical=True)
        # await sub.async_update_layout(10)  # todo resizing
        await sub.async_send_text(f'cd {webPath}\n')
        await sub.async_send_text('yarn dev\n')

        # API

        homesteadPath = '~/homestead'

        await window.async_create_tab()
        session = app.current_window.current_tab.current_session
        await session.async_send_text(f'cd {homesteadPath}\n')
        await session.async_send_text('vagrant up\n')
        await session.async_send_text('vagrant ssh\n')
        await session.async_send_text('cd galaxy-forms-api\n')
        await session.async_send_text('art octane:start\n')

        await asyncio.sleep(30)

        sub2 = await session.async_split_pane(vertical=True)
        await sub2.async_send_text(f'cd {homesteadPath}\n')
        await sub2.async_send_text('vagrant ssh\n')
        await sub2.async_send_text('cd galaxy-forms-api\n')
        await sub2.async_send_text('art horizon\n')

        sub3 = await session.async_split_pane(vertical=True)
        await sub3.async_send_text(f'cd {homesteadPath}\n')
        await sub3.async_send_text('vagrant ssh\n')
        await sub3.async_send_text('cd galaxy-forms-api\n')
        await sub3.async_send_text('art websockets:serve\n')
    else:
        # You can view this message in the script console.
        print("No current window")

# Make a connection to iTerm2 and invoke the main function in an asyncio event loop.
# When main returns the program terminates.
iterm2.run_until_complete(main)
