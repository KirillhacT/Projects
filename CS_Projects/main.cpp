#include <iostream>
#include <vector>
#include <bitset>
#include <assert.h>
#include <fstream>

namespace Core 
{
    template<typename T>    
    void encode(std::vector<int8_t>* buffer, int16_t* iterator, T value)
    {
        for (unsigned i = 0; i < sizeof(T); i++)
        {
            int16_t offset = (sizeof(T) * 8) - (8 * (i + 1));
            (*buffer)[(*iterator)++] = value >> offset;
        }
    }

    template<>
    void encode<float>(std::vector<int8_t>* buffer, int16_t* iterator, float value)
    {
        int32_t result = *reinterpret_cast<int32_t*>(&value);
        encode<int32_t>(buffer, iterator, result);
    }

    template<>
    void encode<double>(std::vector<int8_t>* buffer, int16_t* iterator, double value)
    {
        int32_t result = *reinterpret_cast<int64_t*>(&value);
        encode<int64_t>(buffer, iterator, result);
    }

    template<>
    void encode<std::string>(std::vector<int8_t>* buffer, int16_t* iterator, std::string value)
    {
        for (unsigned i = 0; i < value.size(); i++)
        {
            encode<int8_t>(buffer, iterator, value[i]);
        }
    }

    template<typename T>
    void encode(std::vector<int8_t>* buffer, int16_t* iterator, std::vector<T> value)
    {
        for (unsigned i = 0; i < value.size(); i++)
        {
            encode<T>(buffer, iterator, value[i]);
        }
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
            Root()
                :
                name("unknown"),
                nameLenght(0),
                wrapper(0),
                size(sizeof(nameLenght) + sizeof(wrapper) + sizeof(size)) {} //!
        public:
            int32_t getSize();
            std::string getName();
            void setName(std::string);
            virtual void pack(std::vector<int8_t>*, int16_t*);
    };
    class Primitive : public Root
    {
        private:
            int8_t type = 0;
            std::vector<int8_t>* data = nullptr; //в нее записываем байты значения 
        private:
            Primitive()
            {
                size += sizeof(type);
            };
        public:
            template<typename T>
            static Primitive* create(std::string name, Type type, T value) //Fabric
            {
                Primitive* p = new Primitive();
                p->setName(name);
                p->wrapper = static_cast<int8_t>(Wrapper::PRIMITIVE);
                p->type = static_cast<int8_t>(type);
                p->data = new std::vector<int8_t>(sizeof(value)); //4
                p->size += p->data->size(); //total size -> 17
                int16_t iterator = 0;
                Core::template encode(p->data, &iterator, value);
                return p;
            }
            // static Primitive* createI32(std::string, Type type, int32_t value);
            void pack(std::vector<int8_t>*, int16_t*);
    };
    class Array : public Root
    {

    };
    class Object : public Root
    {

    };
}


namespace Core 
{
    namespace Util
    {
        bool isLittleEndian()
        {
            //0x00 0x00 0x00 0b0000 0101
            int8_t a = 5;
            std::string result = std::bitset<8>(a).to_string();
            if (result.back() == '1') return true;
            return false;
        }
        void save(const char* file, std::vector<int8_t> buffer)
        {
            std::ofstream out;
            out.open(file);
            for (unsigned i = 0; i < buffer.size(); i++)
            {
                out << buffer[i];
            }
            out.close();
        }
        void retriveNsave(ObjectModel::Root* r)
        {
            int16_t iterator = 0;
            std::vector<int8_t> buffer(r->getSize());
            std::string name = r->getName().substr(0, r->getName().length()).append(".ttc");
            r->pack(&buffer, &iterator);
            save(name.c_str(), buffer);
        }

    }
    // buffer = [00000000, 0000000]
    // value = 0100 1000 1000 1000
    // buf[0] = value >> 8 (0100 1000)
    // buf[1] = value 
    //buf -> [01001000, 10001000]

    // void encode16(std::vector<int8_t>* buffer, int16_t* iterator, int16_t value)
    // {
    //     (*buffer)[(*iterator)++] = value;
    // }   (*buffer)[(*iterator)++] = value >> 8;
    //  
}

namespace ObjectModel
{
    //definition Object Model

    
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

    void Root::pack(std::vector<int8_t>*, int16_t*)
    {

    }

    std::string Root::getName()
    {
        return name;
    }

    
    void Primitive::pack(std::vector<int8_t>* buffer, int16_t* iterator)
    {
        Core::encode<std::string>(buffer, iterator, name);
        Core::encode<int16_t>(buffer, iterator, nameLenght);
        Core::encode<int8_t>(buffer, iterator, wrapper);
        Core::encode<int8_t>(buffer, iterator, type);
        Core::encode<int8_t>(buffer, iterator, *data); //Мы разыменовываем весь вектор, а не указатель на 1 эл
        Core::encode<int32_t>(buffer, iterator, size);
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
            // void serialize();
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
using namespace ObjectModel;


int main(int argc, char** argv)
{ 
    assert(Core::Util::isLittleEndian());
    int32_t foo = 12;
    Primitive* p = Primitive::create("int32", Type::I32, foo);
    Core::Util::retriveNsave(p);
    // std::cout << p->getSize() << " " << p->getName() << std::endl;
    // System Foo("foo");
    // Event* e = new KeyBoardEvent('a', true, false);
    // Foo.addEvent(e);
    // KeyBoardEvent* kb = static_cast<KeyBoardEvent*>(Foo.getEvent());
    // std::cout << kb->system->getEvent()->getdType() << std::endl;
}







