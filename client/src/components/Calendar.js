import React from "react";
import FullCalendar from "@fullcalendar/react";
import dayGridPlugin from "@fullcalendar/daygrid";
import timeGridPlugin from "@fullcalendar/timegrid";

const Calendar = ({ sessions }) => {
  // Helpget the initials of the client
  const getClientInitials = name => name.split(" ").map(part => part[0].toUpperCase()).join(".");

  const events = sessions.map(session => {

    const clientInitials = getClientInitials(session.client_name);
    
    
    return {
      title: `${clientInitials}`,
      start: session.date,
    };
  });

  return (
    <FullCalendar
      plugins={[dayGridPlugin, timeGridPlugin]}
      initialView="dayGridMonth"
      events={events}
    />
  );
};

export default Calendar;