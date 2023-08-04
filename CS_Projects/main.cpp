#include <iostream>
#include <vector>

namespace Core 
{
    namespace Util
    {

    }
    // 0 1 2 3
    // 0x00 0x00 0x00 0x05
    // 0x00 0x00 0x00 0x05
    void encode(std::vector<int8_t>* buffer, int16_t* iterator, int32_t value)
    {
        (*buffer)[(*iterator)++] = value >> 24;

    }
}

namespace ObjectModel
{
    enum class Wrapper : int8_t
    {
        PRIMITIVE = 1,
        ARRAY,
        STRING,
        OBJECT
    };

    enum class Type : int8_t
    {
        I8 = 1,
        I16,
        I32,
        I64,
        
        U8,
        U16,
        U32,
        U64,

        FLOAT,
        DOUBLE,
        BOOL
    };

    class Root
    {
        protected:
            std::string name;
            int16_t nameLenght;
            int8_t wrapper; //from enum class Wrapper
            int32_t size;
        protected:
            Root();
        public:
            int32_t getSize();
            void setName(std::string);
            std::string getName();
            virtual void pack(std::vector<int8_t>*, int16_t*);
    };
    class Primitive : public Root
    {
        private:
            int8_t type;
            std::vector<int8_t>* data; //в нее записываем байты значения 
        private:
            Primitive();
        public:
            static Primitive* createI32(std::string, Type type, int32_t value);


    };
    class Array : public Root
    {

    };
    class Object : public Root
    {

    };

    //definition
    Root::Root()
        :
        name("unknown"),
        nameLenght(0),
        wrapper(0),
        size(sizeof nameLenght + sizeof wrapper + sizeof size) {}
    
    void Root::setName(std::string name)
    {
        this->name = name;
        nameLenght = (int16_t)name.length();
        size += nameLenght;
    }

    int32_t Root::getSize()
    {
        return size;
    }

    std::string Root::getName()
    {
        return name;
    }

    Primitive* Primitive::createI32(std::string name, Type type, int32_t value)
    {
        Primitive* p = new Primitive();
        p->setName(name);
        p->wrapper = static_cast<int8_t>(Wrapper::PRIMITIVE);
        p->type = static_cast<int8_t>(type);
        p->data = new std::vector<int8_t>(sizeof value);
        int16_t iterator = 0;
        Core::encode(p->data, &iterator, value);
        return p;
    }
}


namespace EventSystem
{
    class Event;

    class System
    {
        public:
            System(std::string);
            ~System();
        public:
            void addEvent(Event*);
            Event* getEvent();
            bool isActive();
            void serialize();
        private:
            friend class Event;
            std::string name;
            int32_t descriptor;
            int16_t index;
            bool active;
            std::vector<Event*> events;      
    };
    class Event
    {
        public:
            enum DeviceType : int8_t
            {
                KEYBOARD = 1,
                MOUSE,
                TOUCHPAD,
                JOYSTICK,
            };
            DeviceType dType;
            System* system = nullptr;
        public:
            Event(DeviceType);
            DeviceType getdType();
            friend std::ostream& operator<<(std::ostream& stream, const DeviceType dType)
            {
                std::string result;
#define PRINT(a) result = #a;
                switch (dType)
                {
                    case KEYBOARD: PRINT(KEYBOARD); break;
                    case MOUSE: PRINT(KEYBOARD); break;
                    case TOUCHPAD: PRINT(KEYBOARD); break;
                    case JOYSTICK: PRINT(KEYBOARD); break;
                }
                return stream << result;
            }
            void bind(System*, Event*);


    };
    class KeyBoardEvent : public Event
    {
        private:
            int16_t keyCode;
            bool pressed;
            bool released;
        public:
            KeyBoardEvent(int16_t, bool, bool);
            ~KeyBoardEvent();
    };

    //definition

    System::System(std::string) 
    :
    name(name), 
    descriptor(123), 
    index(1),
    active(true) {}

    System::~System()
    {
        //TODO:
    }

    void System::addEvent(Event* e) 
    {
        e->bind(this, e);
    }

    Event* System::getEvent()
    {
        return events.front();
    }

    bool System::isActive()
    {
        if (!system)
            return false;
        return true;
    }

    Event::Event(DeviceType dType)
    {
        this->dType = dType;
    }

    void Event::bind(System* system, Event* event)
    {
        this->system = system;
        this->system->events.push_back(event);
    }


    Event::DeviceType Event::getdType()
    {
        return this->dType;
    }

    KeyBoardEvent::KeyBoardEvent(int16_t keyCode, bool pressed, bool released) 
        :
        Event(Event::KEYBOARD),
        keyCode(keyCode),
        pressed(pressed),
        released(released) {}
}

using namespace EventSystem;

int main(int argc, char** argv)
{
    int32_t foo = 5;
    // System Foo("foo");
    // Event* e = new KeyBoardEvent('a', true, false);
    // Foo.addEvent(e);
    // KeyBoardEvent* kb = static_cast<KeyBoardEvent*>(Foo.getEvent());
    // std::cout << kb->system->getEvent()->getdType() << std::endl;
}







